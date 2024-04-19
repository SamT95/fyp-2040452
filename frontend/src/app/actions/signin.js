"use server"
import { 
    AuthFlowType, 
    CognitoIdentityProviderClient, 
    AdminInitiateAuthCommand 
} from "@aws-sdk/client-cognito-identity-provider";
import { redirect } from "next/navigation";
import { cookies } from "next/headers";

export default async function SignIn(prevState, formData) {
    // Ensure that the code runs on the server-side
    "use server";
    // Instantiate a new Amazon Cognito service client object
    const client = new CognitoIdentityProviderClient({ region: "eu-west-1" });

    // Define the parameters for the AdminInitiateAuthCommand object
    // Pull the user pool ID and app client ID from the environment variables
    // Pull the username and password from the form data
    const signInParams = {
        AuthFlow: AuthFlowType.ADMIN_USER_PASSWORD_AUTH,
        ClientId: process.env.COGNITO_APP_CLIENT_ID,
        UserPoolId: process.env.COGNITO_USER_POOL_ID,
        AuthParameters: {
            USERNAME: formData.get("username"),
            PASSWORD: formData.get("password"),
        }
    };

    let actionOutcome = {
        success: false,
        redirectTo: null,
        cookies: {},
        message: ""
    };

    try {
        // Create a new command object to send the request to the Amazon Cognito service
        const signInCommand = new AdminInitiateAuthCommand(signInParams);
        // Send the request to the Amazon Cognito service
        const response = await client.send(signInCommand);
        // If the request is successful, set the success flag to true and set the message
        actionOutcome.success = true;
        actionOutcome.message = "User signed in successfully. Redirecting...";
        actionOutcome.cookies = response.AuthenticationResult;
        actionOutcome.redirectTo = "/chat";
    } catch (error) {
        // If the request is not successful, set the success flag to false and set the message
        console.error(error);
        actionOutcome.message = `Error signing in user: ${error.message}`;
    }

    if (actionOutcome.success) {
        // Set the cookies in the response headers if the user is signed in successfully
        // Expire tokens in 1 hour
        const expiryDate = new Date(Date.now() + actionOutcome.cookies.ExpiresIn * 1000);
        cookies().set({
            name: "access_token",
            value: actionOutcome.cookies.AccessToken,
            httpOnly: true, // Set the httpOnly flag to true to prevent client-side JavaScript from accessing the cookie
            sameSite: "strict", // Set the SameSite flag to "strict" to prevent CSRF attacks
            secure: true, // Set the secure flag to true to ensure that the cookie is only sent over HTTPS
            expires: expiryDate, // Set the expiration time of the cookie
        })
        redirect(actionOutcome.redirectTo);
    } else {
        return {
            success: false,
            message: actionOutcome.message
        }
    }
}