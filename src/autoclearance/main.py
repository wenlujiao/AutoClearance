#!/usr/bin/env python
import sys
from crewai.flow.flow import Flow, listen, start
from autoclearance.crew import AutoclearanceCrew

def run():
    """
    Run the AutoClearance crew.
    """
    # Simulate raw invoice data with intentional errors for testing
    inputs = {
        'invoice_data': '''
            INVOICE #001
            Desc: Plstic Toys (Kids)
            Qty: 100 pcs
            Unit Price: $5.00
            Total: $400.00  <-- ERROR: Math mismatch (Should be 500)
            GW: 50kg
            NW: 60kg       <-- ERROR: Net Weight > Gross Weight
        '''
    }
    
    AutoclearanceCrew().crew().kickoff(inputs=inputs)