package main

import (
    "context"
    "encoding/json"
    "fmt"
    "log"

    "github.com/minio/madmin-go"
)

func main() {
    // Initialize the MinIO Admin client
    endpoint := "upstash-storage-eu1.api.upstashdev.com"    
    accessKey := "Yh08nykHLkGW0bA0Ou9y"                     
    secretKey := "EpDNNMtmbMb5F36C9PwKBMWIz3aJU8aE1u5YK4GM" 
    secure := true                                          

    client, err := madmin.New(endpoint, accessKey, secretKey, secure)
    if err != nil {
        log.Fatalln(err)
    }

    // Define the policy
    readOnlyPolicy := map[string]interface{}{
        "Version": "2012-10-17",
        "Statement": []map[string]interface{}{
            {
                "Effect": "Allow",
                "Action": []string{
                    "s3:GetBucketLocation",
                    "s3:ListBucket",
                    "s3:GetObject",
                },
                "Resource": []string{
                    "arn:aws:s3:::your-bucket-name",
                    "arn:aws:s3:::your-bucket-name/*",
                },
            },
        },
    }

    policyJSON, err := json.Marshal(readOnlyPolicy)
    if err != nil {
        log.Fatalln(err)
    }

    policyName := "read-only-policy"

    // Add the policy
    err = client.AddCannedPolicy(context.Background(), policyName, policyJSON)
    if err != nil {
        log.Fatalln(err)
    }

    // Create the user
    username := "eray-comp-new-user-hede"
    password := "read-only-password"
    err = client.AddUser(context.Background(), username, password)
    if err != nil {
        log.Fatalln(err)
    }

    // Set the policy to the user
    err = client.SetPolicy(context.Background(), policyName, username, false)
    if err != nil {
        log.Fatalln(err)
    }

    fmt.Printf("User '%s' created with read-only permissions.\n", username)
}