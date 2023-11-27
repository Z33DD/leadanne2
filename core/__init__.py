from postmarker.core import PostmarkClient

from leadanne2.settings import POSTMARK_SERVER_TOKEN

postmark = PostmarkClient(server_token=POSTMARK_SERVER_TOKEN)
