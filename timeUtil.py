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


# Example timestamp in nanoseconds (1523637781405000000)
# nanoseconds = 1523637781405000000
# nanoseconds = 1523637781517000000
nanoseconds = 1557948600000000000


# Convert to LocalDateTime in 'America/New_York'
local_time = convert_nanoseconds_to_localtime(nanoseconds)

# Print the result
print(f"Converted LocalDateTime (America/New_York): {local_time}")