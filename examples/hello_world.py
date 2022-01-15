from time import sleep
from rpa_logger import Logger

l = Logger()

key = l.start_task('Hello world!')

# Sleep 2 seconds to display the progress spinner
sleep(2)

l.finish_task('SUCCESS', key=key)