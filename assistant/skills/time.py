from datetime import datetime
from assistant.skills.decorator import skill


@skill
def get_current_time():
    """Tells the current time. For example:'What time is it?' """
    print(f"The current time is {datetime.now().strftime('%H:%M:%S')}.")