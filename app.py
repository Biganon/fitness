import re
import requests
import secrets
from textual.app import App
from textual.widget import Widget
from textual.widgets import TabbedContent, Log, Footer
from typing import Any, Generator
from http_data import *
from widgets import PlanningTable, BookingsTable

class FitnessApp(App[Any]):
    BINDINGS = [("r", "refresh", "Rafraîchir")]

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.planning_table: PlanningTable = PlanningTable()
        self.bookings_table: BookingsTable = BookingsTable()
        self.logger = Log()
        self.logger.can_focus = False
        self.session = requests.Session()
        self.session.get(splash_url)
        self.j_session_id = self.session.cookies.get("JSESSIONID")
        script_session_id_regex = re.search(r"dwr_scriptSessionId='(.+?)'", self.session.get(customer_url).text)
        self.script_session_id = script_session_id_regex.group(1) if script_session_id_regex else None
        self.session.post(
            url=login_url,
            data=login_data.format(
                self.j_session_id,
                self.script_session_id,
                secrets.PASSWORD,
                secrets.EMAIL,
            ),
        )

    def compose(self) -> Generator[Widget]:
        self.planning_table.add_column("Date")
        self.planning_table.add_column("Heure")
        self.planning_table.add_column("Nom")
        self.planning_table.add_column("Réservations")
        self.planning_table.cursor_type = "row"

        self.bookings_table.add_column("Date")
        self.bookings_table.add_column("Heure")
        self.bookings_table.add_column("Nom")
        self.bookings_table.cursor_type = "row"

        with TabbedContent("Planning", "Réservations"):
            yield self.planning_table
            yield self.bookings_table

        yield self.logger

        yield Footer()

        self.action_refresh()

    def action_refresh(self) -> None:
        self.planning_table.refresh_data()
        self.bookings_table.refresh_data()

    def book(self, identifier: str) -> None:
        self.session.post(
            url=book_url,
            data=book_data.format(
                self.j_session_id,
                self.script_session_id,
                identifier,
                secrets.PID,
            ),
        )
        self.action_refresh()

    def unbook(self, identifier: str) -> None:
        self.session.post(
            url=unbook_url,
            data=unbook_data.format(
                self.j_session_id,
                self.script_session_id,
                identifier,
                secrets.PID,
            ),
        )
        self.action_refresh()