import java.lang.String, jarray
import json
from org.zaproxy.zap.extension.script import ScriptVars
from org.parosproxy.paros.network import HttpRequestHeader, HttpHeader
from org.apache.commons.httpclient import URI
from org.zaproxy.zap.authentication import AuthenticationHelper

def read_mfa_from_file():
    file_path = '/zap/wrk/scripts/mfa'
    try:
        with open(file_path, 'r') as file:
            return file.readline().strip() 
    except Exception as e:
        print("Error reading mfa from file: " + str(e))
        return None

def authenticate(helper, paramsValues, credentials):
    """The authenticate function will be called for authentications made via ZAP."""
    login_msg = helper.prepareMessage()
    login_url = paramsValues.get("loginURL")
    mfa_url = paramsValues.get("mfaURL")

    email = credentials.getParam("email")
    password = credentials.getParam("password")

    login_payload = json.dumps({"email": email, "password": password})
    requestHeader = HttpRequestHeader(HttpRequestHeader.POST, URI(login_url, False), HttpHeader.HTTP11)
    requestHeader.setHeader("Content-Type", "application/json")

    login_msg.setRequestHeader(requestHeader)
    login_msg.setRequestBody(login_payload)
    login_msg.getRequestHeader().setContentLength(len(login_payload))
    
    helper.sendAndReceive(login_msg, True)

    try:
        login_response = json.loads(login_msg.getResponseBody().toString())
        tmpToken = login_response.get("data", {}).get("tmpToken")
        totpToken = read_mfa_from_file()

        if not tmpToken:
            raise Exception("tmpToken missing in login response")

        mfa_msg = helper.prepareMessage()
        mfa_payload = json.dumps({"tmpToken": tmpToken, "totpToken": totpToken})

        mfa_requestHeader = HttpRequestHeader(HttpRequestHeader.POST, URI(mfa_url, False), HttpHeader.HTTP11)
        mfa_requestHeader.setHeader("Content-Type", "application/json")

        mfa_msg.setRequestHeader(mfa_requestHeader)
        mfa_msg.setRequestBody(mfa_payload)
        mfa_msg.getRequestHeader().setContentLength(len(mfa_payload))
        
        helper.sendAndReceive(mfa_msg, True)
        AuthenticationHelper.addAuthMessageToHistory(mfa_msg)
        print("mfa_response", mfa_msg.getResponseBody().toString())
        mfa_response = json.loads(mfa_msg.getResponseBody().toString())
        token = mfa_response.get("authentication", {}).get("token")
        print("token", token)
        if not token:
            raise Exception("Authentication failed")
        return mfa_msg
    except Exception as e:
        print("Authentication failed:", e)
        return None

def getRequiredParamsNames():
    return jarray.array(["loginURL", "mfaURL"], java.lang.String)

def getOptionalParamsNames():
    return jarray.array([], java.lang.String)

def getCredentialsParamsNames():
    return jarray.array(["email", "password"], java.lang.String)
