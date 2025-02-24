import re
import secrets
from datetime import datetime, date, timedelta
from textual import events
from textual.widgets import DataTable
from typing import Any, cast
from http_data import *
from utils import parse_dwr
import app  # need to import entire module to avoid cyclic dependencies

class PlanningTable(DataTable[Any]):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.date = date.today()

    def on_key(self, event: events.Key) -> None:
        if event.key == "right":
            self.date += timedelta(days=1)
            self.refresh_data()
        if event.key == "left":
            self.date -= timedelta(days=1)
            self.refresh_data()

    def on_data_table_row_selected(self, event: DataTable.RowSelected) -> None:
        parent = cast(app.FitnessApp, self.app)
        assert event.row_key.value is not None
        parent.book(event.row_key.value)

    def refresh_data(self) -> None:
        parent = cast(app.FitnessApp, self.app)
        self.clear()
        response = parent.session.post(
            url=planning_url,
            data=planning_data.format(
                parent.j_session_id,
                parent.script_session_id,
                timestamp=int(datetime.combine(self.date, datetime.min.time()).timestamp() * 1000),
            ),
        )
        dwr = parse_dwr(response.text)
        for element in sorted(
            [{
                "id": node["id"],
                "start": node["beginDate"],
                "end": node["endDate"],
                "spotsTotal": (spotsTotal := node["nbPlace"]),
                "spotsTaken": (spotsTaken := node["nbPlaceInUsed"]),
                "spotsFree": spotsTotal - spotsTaken,
                "label": next(dwr[x]["label"] for x in dwr if "cod" in dwr[x] and dwr[x]["cod"] == node["activityIdList"][0]),
            } for node in dwr.values() if "activityIdList" in node],
            key=lambda x: x["start"],
        ):
            taken = element["spotsTaken"]
            total = element["spotsTotal"]
            color = "red" if taken == total else "green"
            self.add_row(
                element["start"].strftime("%A %-d %B"),
                element["start"].strftime("%H:%M"),
                element["label"],
                f"[{color}]{taken:>2}/{total:>2}[/{color}]",
                key=element["id"],
            )

class BookingsTable(DataTable[Any]):
    def on_data_table_row_selected(self, event: DataTable.RowSelected) -> None:
        parent = cast(app.FitnessApp, self.app)
        assert event.row_key.value is not None
        parent.unbook(event.row_key.value)

    def refresh_data(self) -> None:
        self.clear()
        parent = cast(app.FitnessApp, self.app)
        response = parent.session.post(
            url=bookings_url,
            data=bookings_data.format(
                parent.j_session_id,
                parent.script_session_id,
                secrets.PID,
            ),
        )
        dwr = parse_dwr(response.text)
        # open("/tmp/prout.json", "w").write(json.dumps(dwr, default=lambda x: '<not serializable>'))
        for element in sorted(
            [{
                "id": node["bookingId"],
                "start": node["bookingBeginDate"],
                "end": node["bookingEndDate"],
                "activity_id": node["bookingForPlanning"]["activityIdList"][0],
            } for node in dwr["s0"]],
            key=lambda x: x["start"],
        ):
            activity_response = parent.session.post(
                url=activity_url,
                data=activity_data.format(
                    parent.j_session_id,
                    parent.script_session_id,
                    element["activity_id"],
                ),
            )
            label_regex = re.search(r'name:"(.*?)"', activity_response.text)
            label = label_regex.group(1) if label_regex else None
            self.add_row(
                element["start"].strftime("%A %-d %B"),
                element["start"].strftime("%H:%M"),
                label,
                key=element["id"],
            )
