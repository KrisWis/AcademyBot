from datetime import datetime
import pytz

def nowIsSupportGraphic() -> bool:
    moscow_tz = pytz.timezone('Europe/Moscow')

    moscow_time = datetime.now(moscow_tz)

    start_time = moscow_time.replace(hour=10, minute=0, second=0, microsecond=0)
    end_time = moscow_time.replace(hour=22, minute=0, second=0, microsecond=0)

    if start_time <= moscow_time <= end_time:
        return True
    else:
        return False