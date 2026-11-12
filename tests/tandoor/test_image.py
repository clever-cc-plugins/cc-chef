import http.client
import io
import os
import socket
import unittest
from contextlib import redirect_stderr, redirect_stdout
from unittest import mock

import tandoor
import tandoor_client as tc
import tandoor_image as ti
from helpers import TOKEN, FakeCase, ImageHost


class FetchTests(unittest.TestCase):
    def setUp(self):
        self.host = ImageHost()
        self.addCleanup(self.host.stop)

    def test_loopback_is_refused_by_default(self):
        with self.assertRaisesRegex(tc.TandoorError, "not a public address"):
            ti.fetch(self.host.url + "/ok.jpg")

    def test_only_http_and_https(self):
        for url in ("file:///etc/passwd", "ftp://example.com/a.jpg", "javascript:1"):
            with self.assertRaises(tc.TandoorError):
                ti.check_scheme(url)

    def test_fetch_follows_checked_redirect_and_rejects_the_rest(self):
        with mock.patch.object(ti, "public_addresses", lambda h, port=0: ["127.0.0.1"]):
            self.assertEqual(ti.fetch(self.host.url + "/go"), (b"\xff\xd8\xff\xd9", "image/jpeg"))
            for path, message in (("/page", "not a jpeg"), ("/big.jpg", "larger than"), ("/file", "image download failed")):
                with self.assertRaisesRegex(tc.TandoorError, message):
                    ti.fetch(self.host.url + path)

    def test_redirect_target_is_checked_again(self):
        public = lambda h, port=0: ["127.0.0.1"] if h == "localhost" else []  # noqa: E731  first hop passes, the redirect to 127.0.0.1 does not
        with mock.patch.object(ti, "public_addresses", public):
            with self.assertRaisesRegex(tc.TandoorError, "not a public address"):
                ti.fetch(self.host.url.replace("127.0.0.1", "localhost") + "/go-private")

    def test_connection_dials_the_checked_address_not_the_hostname(self):
        port = int(self.host.url.rsplit(":", 1)[1])
        with mock.patch.object(ti, "public_addresses", lambda h, p=0: ["127.0.0.1"]):
            with mock.patch("socket.create_connection", wraps=socket.create_connection) as conn:
                ti.fetch("http://pinned.example:%d/ok.jpg" % port)
        self.assertEqual(conn.call_args[0][0], ("127.0.0.1", port))

    def test_connect_time_lookup_is_checked_too(self):
        with mock.patch.object(ti, "_check"), mock.patch.object(ti, "public_addresses", lambda h, p=0: []):
            with self.assertRaisesRegex(tc.TandoorError, "not a public address"):
                ti.fetch("http://rebind.example/ok.jpg")

    def test_incomplete_read_is_a_tandoor_error(self):
        resp = mock.MagicMock()
        resp.__enter__.return_value = resp
        resp.headers = {"Content-Type": "image/jpeg"}
        resp.read.side_effect = http.client.IncompleteRead(b"x")
        with mock.patch.object(ti, "_check"), mock.patch("urllib.request.OpenerDirector.open", return_value=resp):
            with self.assertRaisesRegex(tc.TandoorError, "image download failed"):
                ti.fetch("http://example.com/a.jpg")


class UploadImageTests(FakeCase):
    def setUp(self):
        super().setUp()
        self.images = ImageHost()
        self.addCleanup(self.images.stop)

    def run_main(self, *args):
        env = {**{k: v for k, v in os.environ.items() if not k.startswith("TANDOOR_")}, "TANDOOR_URL": self.url, "TANDOOR_API_TOKEN": TOKEN}
        out, err = io.StringIO(), io.StringIO()
        with mock.patch.dict(os.environ, env, clear=True), mock.patch.object(ti, "public_addresses", lambda h, port=0: ["127.0.0.1"]):
            with redirect_stdout(out), redirect_stderr(err):
                code = tandoor.main([str(a) for a in args])
        return code, out.getvalue(), err.getvalue()

    def prepare(self, image):
        code, _, err = self.run_main("match", self.recipe, "-o", self.plan_path, *(["--image-url", self.images.url + image] if image else []))
        self.assertEqual(code, 0, err)
        self.resolve_all()
        code, out, err = self.run_main("preview", self.plan_path)
        self.assertEqual(code, 0, out + err)
        return out.split("Confirm: ")[1].split()[0], out

    def put_requests(self):
        return [r for r in self.fake.requests if r["method"] == "PUT" and r["path"].endswith("/image/")]

    def test_image_is_shown_in_preview_and_attached(self):
        digest, preview = self.prepare("/ok.jpg")
        self.assertIn("Image: downloaded from " + self.images.url + "/ok.jpg", preview)
        code, out, err = self.run_main("upload", self.plan_path, "--confirm", digest)
        self.assertEqual(code, 0, err)
        self.assertIn("Image: set from the source page", out)
        (put,) = self.put_requests()
        self.assertIn(b"\xff\xd8\xff\xd9", put["body"])
        self.assertNotIn(TOKEN.encode(), put["body"])
        self.assertTrue(self.fake.db["recipe"][-1]["image"])

    def test_no_image_url_means_no_image_request(self):
        digest, preview = self.prepare(None)
        self.assertNotIn("Image:", preview)
        code, _, err = self.run_main("upload", self.plan_path, "--confirm", digest)
        self.assertEqual(code, 0, err)
        self.assertEqual(self.put_requests(), [])

    def test_image_url_changes_the_confirmation_code(self):
        with_image, _ = self.prepare("/ok.jpg")
        without, _ = self.prepare(None)
        self.assertNotEqual(with_image, without)

    def test_failed_image_keeps_the_saved_recipe(self):
        digest, _ = self.prepare("/page")
        code, out, err = self.run_main("upload", self.plan_path, "--confirm", digest)
        self.assertEqual(code, 0, err)
        self.assertIn("Created:", out)
        self.assertIn("Image not set:", err)
        self.assertEqual(self.put_requests(), [])

    def test_match_refuses_image_url_for_an_update(self):
        self.recipe.write_text(self.recipe.read_text(encoding="utf-8").replace("---\n", "---\ntandoor-id: 5\n", 1), encoding="utf-8")
        code, _, err = self.run_main("match", self.recipe, "-o", self.plan_path, "--image-url", self.images.url + "/ok.jpg")
        self.assertEqual(code, 1)
        self.assertIn("new recipes only", err)

    def test_match_refuses_a_non_http_image_url(self):
        code, _, err = self.run_main("match", self.recipe, "-o", self.plan_path, "--image-url", "file:///etc/passwd")
        self.assertEqual(code, 1)
        self.assertIn("http", err)


if __name__ == "__main__":
    unittest.main()
