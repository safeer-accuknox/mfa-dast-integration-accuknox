import java.lang.String, jarray
import json
import org.zaproxy.zap.extension.script.ScriptVars as ScriptVars
from org.parosproxy.paros.network import HtmlParameter, HttpRequestHeader
from org.parosproxy.paros.network.HtmlParameter import Type

def extractWebSession(sessionWrapper):
    """Extract the authentication token from the response."""
    responseBody = sessionWrapper.getHttpMessage().getResponseBody().toString()
    
    try:
        jsonResponse = json.loads(responseBody)
        token = jsonResponse.get('authentication', {}).get('token')
        
        if token:
            sessionWrapper.getSession().setValue("token", token)
            ScriptVars.setGlobalVar("juiceshop.token", token)
        else:
            print("[extractWebSession] No token found in the response.")
    except Exception as e:
        print("[extractWebSession] Error parsing JSON:", str(e))

def clearWebSessionIdentifiers(sessionWrapper):
    """Clear the authentication token and headers."""
    msg = sessionWrapper.getHttpMessage()
    msg.getRequestHeader().setHeader("Authorization", None)
    ScriptVars.setGlobalVar("juiceshop.token", None)

def processMessageToMatchSession(sessionWrapper):
    """Process the message to include the authentication token."""
    token = ScriptVars.getGlobalVar("juiceshop.token")
    
    if token is None:
        print('[processMessageToMatchSession] No token found.')
        return

    msg = sessionWrapper.getHttpMessage()
    msg.getRequestHeader().setHeader("Authorization", "Bearer " + token)
    
    cookie = HtmlParameter(Type.cookie, "token", token)
    cookies = msg.getRequestHeader().getCookieParams()
    cookies.add(cookie)
    msg.getRequestHeader().setCookieParams(cookies)


def getRequiredParamsNames():
    """Returns required parameter names."""
    return jarray.array([], java.lang.String)  # No required params for this script

def getOptionalParamsNames():
    """Returns optional parameter names."""
    return jarray.array([], java.lang.String)  # No optional params for this script

def getCredentialsParamsNames():
    """Returns credential parameter names."""
    return jarray.array([], java.lang.String)  # No credential params needed for this script
