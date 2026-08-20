import ast
import unittest

from domonic.ext import (
    get_hello_world,
    get_server_requirements,
    get_supported_servers,
)


class TestExtScaffolds(unittest.TestCase):
    def test_supported_servers_are_scaffolded(self):
        servers = get_supported_servers()
        self.assertIn("none", servers)
        self.assertIn("fastapi", servers)
        self.assertIn("fasthtml", servers)
        self.assertIn("apiflask", servers)
        self.assertIn("django-ninja", servers)
        self.assertIn("muffin", servers)
        self.assertIn("baize", servers)
        self.assertIn("esmerald", servers)
        self.assertIn("granian", servers)
        self.assertIn("emmett", servers)
        self.assertIn("eve", servers)
        self.assertIn("klein", servers)
        self.assertIn("litestar", servers)
        self.assertIn("robyn", servers)

        for server in servers:
            if server == "none":
                self.assertEqual(get_server_requirements(server), [])
                self.assertIsNone(get_hello_world(server))
                continue

            requirements = get_server_requirements(server)
            hello_world = get_hello_world(server)

            self.assertTrue(requirements, server)
            self.assertIsNotNone(hello_world, server)
            self.assertIn("domonic.html", hello_world, server)
            self.assertIn("html(", hello_world, server)
            self.assertIn("Generated with domonic.html.", hello_world, server)

    def test_server_requirements_are_pinned(self):
        for server in get_supported_servers():
            for requirement in get_server_requirements(server):
                self.assertIn("==", requirement, requirement)

    def test_hello_world_templates_are_valid_python(self):
        for server in get_supported_servers():
            hello_world = get_hello_world(server)
            if hello_world is None:
                continue
            with self.subTest(server=server):
                ast.parse(hello_world)

    def test_modern_server_scaffolds_use_current_packages(self):
        self.assertEqual(get_server_requirements("fasthtml"), ["python-fasthtml==0.14.12"])
        self.assertEqual(get_server_requirements("apiflask"), ["APIFlask==3.1.1"])
        self.assertIn("django-ninja==1.6.3", get_server_requirements("django-ninja"))
        self.assertEqual(get_server_requirements("esmerald"), ["esmerald==3.9.4", "lilya==0.23.3", "uvicorn==0.52.4"])
        self.assertEqual(get_server_requirements("granian"), ["granian==2.8.1"])

    def test_non_one_file_targets_are_not_scaffolded(self):
        servers = get_supported_servers()
        for package in (
            "connexion",
            "daphne",
            "gradio",
            "graphene",
            "gunicorn",
            "httpx",
            "invenio",
            "jupyterhub",
            "kombu",
            "masonite",
            "motor",
            "nicegui",
            "pydantic",
            "py4web",
            "reflex",
            "shiny",
            "streamlit",
            "trio",
            "uvicorn",
            "waitress",
        ):
            self.assertNotIn(package, servers)


if __name__ == "__main__":
    unittest.main()
