"use server"
import {
    CognitoIdentityProviderClient,
    SignUpCommand,
    ConfirmSignUpCommand
} from "@aws-sdk/client-cognito-identity-provider";

export async function Register(prevState, formData) {
    "use server";
    const rawFormData = {
        email: formData.get("email"),
        username: formData.get("username"),
        password: formData.get("password"),
    };

    const client = new CognitoIdentityProviderClient({ region: "eu-west-1" });

    const signUpParams = {
        ClientId: process.env.COGNITO_APP_CLIENT_ID,
        Username: rawFormData.username,
        Password: rawFormData.password,
        UserAttributes: [
            { Name: "email", Value: rawFormData.email },
        ]
    };

    try {
        const signUpCommand = new SignUpCommand(signUpParams);
        await client.send(signUpCommand);
        return {
            success: true,
            message: "Success! Please enter the verification code sent to your email below."
        }
    } catch (error) {
        console.error(error);
        return {
            success: false,
            message: `Error registering user: ${error.message}`
        }
    }
}

export async function Verify(prevState, formData) {
    "use server";
    const rawFormData = {
        username: formData.get("username"),
        code: formData.get("code")
    };

    const client = new CognitoIdentityProviderClient({ region: "eu-west-1" });

    const confirmSignUpParams = {
        ClientId: process.env.COGNITO_APP_CLIENT_ID,
        Username: rawFormData.username,
        ConfirmationCode: rawFormData.code
    };

    try {
        const confirmSignUpCommand = new ConfirmSignUpCommand(confirmSignUpParams);
        await client.send(confirmSignUpCommand);
        return {
            success: true,
            message: "Success! Please sign in with your new account."
        }
    } catch (error) {
        console.error(error);
        return {
            success: false,
            message: `Error verifying user: ${error.message}`
        }
    }
}