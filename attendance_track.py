from datetime import datetime
import pandas as pd

class AttendanceTracker: 
    def __init__(self) -> None: 
        self._attendance = {}

    def mark_attendance(self, name: str) -> None: 
        if name != "unfamiliar" and name not in self._attendance: 
            self._attendance[name] = datetime.now().isoformat()

    def save_attendance(self, filepath: str = "attendance.csv") -> None:
        df = pd.DataFrame(self._attendance.items(), columns=["Name", "Time"])
        df.to_csv(filepath, index=False)


