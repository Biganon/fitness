splash_url = "https://wellness-sportclub.resamania.fr/login/"
customer_url = "https://wellness-sportclub.resamania.fr/customer.js"
login_url = "https://wellness-sportclub.resamania.fr/dwr/call/plaincall/RightRemote.authenticate.dwr"
planning_url = "https://wellness-sportclub.resamania.fr/dwr/call/plaincall/OnlineRemote.initializePlanning.dwr"
bookings_url = "https://wellness-sportclub.resamania.fr/dwr/call/plaincall/ParticipanthistoryRemote.listNextBooking.dwr"
activity_url = "https://wellness-sportclub.resamania.fr/dwr/call/plaincall/ResamaniaRemote.getActivity.dwr"
book_url = "https://wellness-sportclub.resamania.fr/dwr/call/plaincall/OnlineRemote.bookForCustomer.dwr"
unbook_url = "https://wellness-sportclub.resamania.fr/dwr/call/plaincall/OnlineRemote.unbookForCustomer.dwr"

login_data = """
callCount=1
httpSessionId={}
scriptSessionId={}
c0-scriptName=RightRemote
c0-methodName=authenticate
c0-id=0
c0-param0=Object_AuthenticationRequest:{{password:string:{}, mail:string:{}}}
c0-param1=boolean:false
c0-param2=boolean:false
c0-param3=boolean:false
batchId=4
"""

planning_data = """
callCount=1
httpSessionId={}
scriptSessionId={}
c0-scriptName=OnlineRemote
c0-methodName=initializePlanning
c0-id=0
c0-param0=boolean:false
c0-e3=Object_FilterValueEntry:{{typeOfSelection:string:roomSelector, selected:number:5574}}
c0-e9=Object_FilterValueEntry:{{typeOfSelection:string:activitySelector, selected:number:-1}}
c0-e15=Object_FilterValueEntry:{{typeOfSelection:string:coachSelector, selected:number:-1}}
c0-e2=Array:[reference:c0-e3,reference:c0-e9,reference:c0-e15]
c0-e23=Object_Object:{{firstDay:Date:{timestamp}, lastDay:Date:{timestamp}}}
c0-param1=Object_FilterValue:{{entries:reference:c0-e2, activitySupplierId:null:null, roomSupplierId:null:null, calendarEntry:reference:c0-e23}}
c0-param2=number:6003317
batchId=15
"""

bookings_data = """
callCount=1
page=/onlineV2/index.html
httpSessionId={}
scriptSessionId={}
c0-scriptName=ParticipanthistoryRemote
c0-methodName=listNextBooking
c0-id=0
c0-param0=number:{}
c0-param1=number:0
c0-param2=number:1000
c0-param3=boolean:false
batchId=6
"""

activity_data = """
callCount=1
page=/onlineV2/index.html
httpSessionId={}
scriptSessionId={}
c0-scriptName=ResamaniaRemote
c0-methodName=getActivity
c0-id=0
c0-param0=number:{}
batchId=7
"""

book_data = """
callCount=1
httpSessionId={}
scriptSessionId={}
c0-scriptName=OnlineRemote
c0-methodName=bookForCustomer
c0-id=0
c0-param0=boolean:false
c0-param1=number:{}
c0-param2=number:{}
c0-param3=number:1
batchId=59
"""

unbook_data = """
callCount=1
page=/onlineV2/index.html
httpSessionId={}
scriptSessionId={}
c0-scriptName=OnlineRemote
c0-methodName=unbookForCustomer
c0-id=0
c0-param0=boolean:false
c0-param1=number:{}
c0-param2=number:{}
batchId=42
"""