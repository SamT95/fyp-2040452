"use client"
import styles from "./DeploymentStatus.module.css";
import useDeploymentStatus from "@/app/hooks/useDeploymentStatus";

export default function DeploymentStatus() {
    const { deploymentStatus } = useDeploymentStatus();
    const deployed = deploymentStatus === 200 ? true : false;
    return (
        <div className={styles.deploymentStatusContainer}>
            {/* <button onClick={handleOpen} className={styles.button}>Check Deployment Status</button> */}
                <div className={styles.deploymentStatus}>
                    <p>Status: {deployed ? "Deployed" : "Not Deployed"}</p>
                    <span className={styles.statusIcon} style={{ backgroundColor: deployed ? "green" : "red" }}></span>
                </div>
        </div>
    )
}