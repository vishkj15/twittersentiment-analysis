import facebook
import dateutil.parser as dateparser
from pylab import *
from nltk.sentiment.vader import SentimentIntensityAnalyzer


#  here is token which you get from Facebook Graph APIs, every time using program, you need update this token
token = "EAAQFTXtfUVsBAL7maVcQPit3ZA43hAZAtwhou0XV1pXnQbi1PGDrG2q68ZA0rtqdNVRrEeyejFFSHVIM7ANYKYseZCahuFFEmdh0QPcpkzSJZArBZB0tQ7RfGZBRtqHVuQudVwD63p5wHTXjNE6OPm4iatDbZCMVZCzJGdfPDYxYqZBa9Y2IXHx1wfio57ZBguDD6b3i9Gkfpy4v0f0dLOgQVecwXxBAZBvJIFmu27NBI39i0QZDZD"
graph = facebook.GraphAPI(token)
# here is a array of post_ids
# The 1st ID is BBC, the 2nd ID is CNN
post_ids = [
            '-53914757'
            # '1143803202301544_10153361940712217',
            # '5550296508_10154411968366509'
           ]
post_titles = [
                
                ''
              ]
posts = graph.get_objects(ids=post_ids)
