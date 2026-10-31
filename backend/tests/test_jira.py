"""Tests des Jira-Pushs ohne echtes Jira: httpx.MockTransport spielt Jira nach."""
import json

import httpx

from app.jira.adapter import JiraAdapter, JiraError, render_description
from app.jira.router import get_tracker
from app.main import app
from fastapi.testclient import TestClient

PROJECT = {"issueTypes": [
    {"id": "10", "name": "Epic", "subtask": False, "hierarchyLevel": 1},
    {"id": "11", "name": "Task", "subtask": False, "hierarchyLevel": 0},
    {"id": "12", "name": "Subtask", "subtask": True, "hierarchyLevel": -1},
]}


def make(handler):
    return JiraAdapter("https://x.atlassian.net/", "a@b.de", "tok", "atl", transport=httpx.MockTransport(handler))


def test_describe_picks_types_and_falls_back_to_task():
    def h(req):
        assert req.url.path == "/rest/api/2/project/ATL"
        return httpx.Response(200, json=PROJECT)
    d = make(h).describe()
    assert d["epic_type"] == "Epic" and d["story_type"] == "Task" and d["project_key"] == "ATL"


def test_create_epic_then_story_with_parent():
    sent = []

    def h(req):
        if req.method == "GET":
            return httpx.Response(200, json=PROJECT)
        body = json.loads(req.content)
        sent.append(body["fields"])
        return httpx.Response(201, json={"key": f"ATL-{len(sent)}"})
    a = make(h)
    e = a.create_epic("Epic A", render_description("Text"))
    s = a.create_story("Story B", render_description("Als X", ["K1", "K2"]), e.key)
    assert e.key == "ATL-1" and s.url == "https://x.atlassian.net/browse/ATL-2"
    assert sent[0]["issuetype"]["id"] == "10" and "parent" not in sent[0]
    assert sent[1]["parent"] == {"key": "ATL-1"} and sent[1]["issuetype"]["id"] == "11"
    assert "* K1" in sent[1]["description"] and "Akzeptanzkriterien" in sent[1]["description"]


def test_error_messages_are_friendly():
    for code, text in ((401, "Anmeldung"), (403, "Zugriff"), (404, "nicht gefunden")):
        try:
            make(lambda r, c=code: httpx.Response(c, json={})).describe()
            assert False
        except JiraError as e:
            assert text in str(e)


class FakeTracker:
    def __init__(self, fail_on=None):
        self.n = 0; self.fail_on = fail_on

    def describe(self):
        return {"project_key": "ATL"}

    def _ref(self):
        from app.jira.port import IssueRef
        self.n += 1
        if self.fail_on == self.n:
            raise JiraError("kaputt")
        return IssueRef(f"ATL-{self.n}", f"https://x/browse/ATL-{self.n}")

    def create_epic(self, t, d):
        return self._ref()

    def create_story(self, t, d, k):
        return self._ref()


BODY = {"epics": [{"title": "E", "description": "d", "requirements": [{"title": "R", "description": "d", "criteria": ["a"]}]}]}


def test_push_endpoint_success_and_partial_failure():
    app.dependency_overrides[get_tracker] = lambda: FakeTracker()
    r = TestClient(app).post("/api/jira/push", json=BODY).json()
    assert [c["key"] for c in r["created"]] == ["ATL-1", "ATL-2"] and r["failed"] is None
    app.dependency_overrides[get_tracker] = lambda: FakeTracker(fail_on=2)
    r = TestClient(app).post("/api/jira/push", json=BODY).json()
    assert len(r["created"]) == 1 and r["failed"] == "kaputt"
    app.dependency_overrides[get_tracker] = lambda: None
    c = TestClient(app)
    assert c.get("/api/jira/status").json()["configured"] is False
    assert c.post("/api/jira/push", json=BODY).status_code == 400
    app.dependency_overrides.clear()
