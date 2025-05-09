class Logger:
    def __init__(self, log_file="/var/log/nullfrog.log"):
        self.log_file = log_file

    def log_suspicious_activity(self, message):
        print(message)  # For demo visibility
        try:
            with open(self.log_file, "a") as f:
                f.write(message + "\n")
        except Exception as e:
            print(f"[Logger] Failed to write to log file: {e}") 

            

#TODO:replace with aws cloudtrail