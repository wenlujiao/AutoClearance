import sys
from autoclearance.crew import AutoclearanceCrew

def run():
 
    raw_invoice_text = """
    INVOICE #001
    Desc: Plastic Toys (Kids)
    Qty: 100 pcs
    Unit Price: $5.00
    Total: $400.00
    GW: 50kg
    NW: 60kg
    """

    inputs = {
        'invoice_data': raw_invoice_text
    }

    print("🚀 Starting AutoClearance System...")


    while True:
    
        result = AutoclearanceCrew().crew().kickoff(inputs=inputs)
        
    
        result_str = str(result)

    
        if "Risk Alert" in result_str or "FAILED" in result_str:
            print("\n" + "="*50)
            print("⚠️  SYSTEM ALERT: Compliance Risk Detected. Process Paused.")
            print("="*50)
            print(f"Error Details:\n{result_str}\n")
            
           
            print(">>> Action Required: Please manually correct the weight data.")
            
        
            new_gw = input("Enter correct Gross Weight (GW): ")
            new_nw = input("Enter correct Net Weight (NW): ")
            
            print("\n🔄 Updating data and re-running the audit agent...\n")
            
        
            updated_data = f"""
            INVOICE #001
            Desc: Plastic Toys (Kids)
            Qty: 100 pcs
            Unit Price: $5.00
            Total: $500.00
            GW: {new_gw}kg  <-- Manual Correction
            NW: {new_nw}kg  <-- Manual Correction
            """
            
            inputs['invoice_data'] = updated_data
            
            continue

        else:
            print("\n" + "="*50)
            print("✅ AUDIT PASSED. No risks detected.")
            print("="*50)
            print(result)
            break