from supabase import create_client

# Replace with your actual Supabase credentials
url = "https://mwqgjwirrsauufbihoyq.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im13cWdqd2lycnNhdXVmYmlob3lxIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2NTMzMDEwMywiZXhwIjoyMDgwOTA2MTAzfQ.3LtVF_1ZYyMjC_EMRPJjqk6MYg4oexfa0J3o9q12aGo"

supabase = create_client(url, key)

# Test a simple query
response = supabase.table("telco_churn1").select("*").limit(1).execute()
print(response)


