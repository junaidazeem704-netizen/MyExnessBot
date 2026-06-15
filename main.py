def execute_direct_exness_trade(symbol, direction, lot, sl, tp):
    """
    Directly connects to Exness Web Trading API endpoints using account credentials.
    Authenticates and executes market orders live on your Exness Standard Account.
    """
    try:
        session = requests.Session()
        
        # 🔒 Step 1: Authentication Handshake with Exness Secure Gateway
        # Exness Web terminal endpoints authorize your connection here securely
        auth_url = "https://webterminal.exness.com/api/v1/auth/login"
        auth_payload = {
            "login": EXNESS_ACCOUNT,
            "password": EXNESS_PASSWORD
        }
        
        print(f"🔐 Authenticating with Exness Server for Account: {EXNESS_ACCOUNT}...")
        auth_response = session.post(auth_url, json=auth_payload, timeout=10)
        
        if auth_response.status_code != 200:
            print("❌ Exness Authentication Failed. Please check your MT5 password or account number.")
            return False, "Auth Failed"
            
        # Extracting security token safely from session headers
        token = auth_response.json().get("token")
        headers = {"Authorization": f"Bearer {token}"}
        
        # 📈 Step 2: Route Order Parameters to Exness Trade Terminal Matrix
        order_url = "https://webterminal.exness.com/api/v1/orders"
        
        # Mapping trade directions (0 for BUY, 1 for SELL)
        cmd_action = 0 if direction == 1 else 1
        
        order_payload = {
            "account": int(EXNESS_ACCOUNT),
            "symbol": symbol,
            "operation": cmd_action,
            "volume": lot,
            "stopLoss": sl,
            "takeProfit": tp,
            "type": "MARKET"
        }
        
        print(f"📡 Dispatching Live Order: {symbol} | Lot: {lot} | Action: {'BUY' if direction==1 else 'SELL'}...")
        order_response = session.post(order_url, json=order_payload, headers=headers, timeout=10)
        
        if order_response.status_code in [200, 201]:
            order_id = order_response.json().get("orderId", "LiveTrade")
            print(f"✅ Exness Order Placed Successfully! Ticket ID: {order_id}")
            return True, "Success"
        else:
            error_details = order_response.text
            print(f"❌ Exness Execution Refused: {error_details}")
            return False, f"Server Refused: {order_response.status_code}"
            
    except Exception as e:
        print(f"Direct Exness Gateway System Error: {e}")
        return False, str(e)
