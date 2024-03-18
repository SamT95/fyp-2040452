// Hook for sending messages in the chat window
// and updating the Zustand store with the new message
"use client"
import { useEffect, useState } from "react";

export default function useDeploymentStatus() {
    const [deploymentStatus, setDeploymentStatus] = useState(null);
    useEffect(() => {
        async function fetchDeploymentStatus() {
            try {
                const response = await fetch("/api/status");
                const data = await response.json();
                setDeploymentStatus(data.status);
            } catch (error) {
                console.error("Failed to fetch deployment status:", error);
                setDeploymentStatus(false);
            }
        }
        fetchDeploymentStatus();
    }, []);

    return {
        deploymentStatus,
    };
}
