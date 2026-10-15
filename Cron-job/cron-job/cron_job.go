package main

import (
	"log"
	"os"
	"os/exec"

	"github.com/robfig/cron/v3"
)

func main() {
	// Create a new cron scheduler
	c := cron.New()

	// Add your task to run the fetch_google_sheets_docs.py script every 5 minutes
	_, err := c.AddFunc("*/5 * * * *", func() {
		// Run the Python script every 5 minutes
		runPythonScript()
	})
	if err != nil {
		log.Fatalf("Error scheduling task: %v", err)
	}

	// Start the cron job scheduler
	c.Start()

	// Run indefinitely to keep the cron jobs running
	log.Println("Cron job scheduler started...")
	select {}
}

// Function to run the Python script
func runPythonScript() {
	// Define the path to your Python script
	scriptPath := `C:\Users\Checkout\cron-job-service\scripts\fetch_google_sheets_docs.py`

	// If you're using a virtual environment, point to the Python executable inside the venv
	// Adjust the path to your Python interpreter in the virtual environment
	pythonExec := `C:\Users\Checkout\cron-job-service\venv\Scripts\python` // Modify this to the correct path

	// Prepare the command to execute the Python script
	cmd := exec.Command(pythonExec, scriptPath)

	// Set up the output (stdout and stderr)
	cmd.Stdout = os.Stdout
	cmd.Stderr = os.Stderr

	// Execute the command
	err := cmd.Run()
	if err != nil {
		log.Printf("Error running Python script: %v", err)
	} else {
		log.Println("Python script executed successfully.")
	}
}
