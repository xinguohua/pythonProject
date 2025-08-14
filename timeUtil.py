from datetime import datetime, timezone, timedelta
import pytz


# Function to convert nanoseconds to LocalDateTime in the 'America/New_York' timezone
def convert_nanoseconds_to_localtime(nanoseconds):
    # Convert nanoseconds to seconds and nanoseconds
    seconds = nanoseconds // 1_000_000_000
    nano_adjustment = nanoseconds % 1_000_000_000

    # Create a datetime object using the seconds part
    dt = datetime.utcfromtimestamp(seconds)

    # Adjust for nanoseconds
    dt = dt.replace(microsecond=nano_adjustment // 1000)  # Converting nanoseconds to microseconds

    # Set the timezone to UTC
    dt_utc = dt.replace(tzinfo=timezone.utc)

    # Convert to 'America/New_York' timezone
    new_york_tz = pytz.timezone("America/New_York")
    dt_ny = dt_utc.astimezone(new_york_tz)

    return dt_ny


def convert_localtime_to_nanoseconds(year, month, day, hour, minute, second, microsecond=0):
    new_york_tz = pytz.timezone("America/New_York")
    dt_ny = datetime(year, month, day, hour, minute, second, microsecond, tzinfo=new_york_tz)

    # 转换到 UTC
    dt_utc = dt_ny.astimezone(timezone.utc)

    # 转为秒级时间戳
    seconds = int(dt_utc.timestamp())

    # 纳秒级计算
    nanoseconds = seconds * 1_000_000_000 + dt_utc.microsecond * 1_000
    return nanoseconds


# Example timestamp in nanoseconds (1523637781405000000)
# nanoseconds = 1523637781405000000
# nanoseconds = 1523637781517000000
# nanoseconds = 1558105200000000000
# local_time = convert_nanoseconds_to_localtime(nanoseconds)
# print(f"Converted LocalDateTime (America/New_York): {local_time}")

nano_ts = convert_localtime_to_nanoseconds(2019, 5, 17, 10, 10, 0)
print(nano_ts)
nano_ts = convert_localtime_to_nanoseconds(2019, 5, 17, 14, 30, 0)
print(nano_ts)