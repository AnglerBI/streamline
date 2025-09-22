import os
import streamlit as st
from supabase import create_client, Client
from typing import Optional, Dict, Any

class SupabaseClient:
    def __init__(self):
        self.url = os.getenv("SUPABASE_URL") or st.secrets.get("SUPABASE_URL")
        self.key = os.getenv("SUPABASE_ANON_KEY") or st.secrets.get("SUPABASE_ANON_KEY")

        if not self.url or not self.key:
            st.error("Supabase credentials not found. Please check your environment variables or secrets.")
            st.stop()

        self.client: Client = create_client(self.url, self.key)

    def register_user(self, email: str, phone: str, password: str) -> Dict[str, Any]:
        """Register a new user with email, phone and password"""
        try:
            response = self.client.auth.sign_up({
                "email": email,
                "password": password,
                "options": {
                    "data": {
                        "phone_number": phone
                    }
                }
            })

            # Sign in immediately after registration (since email confirmation is disabled)
            if response.user:
                sign_in_response = self.client.auth.sign_in_with_password({
                    "email": email,
                    "password": password
                })
                return {"success": True, "user": sign_in_response.user, "session": sign_in_response.session}

            return {"success": True, "user": response.user}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def sign_in_user(self, email_or_phone: str, password: str) -> Dict[str, Any]:
        """Sign in existing user with email or phone"""
        try:
            # If it looks like an email, use it directly
            if "@" in email_or_phone:
                response = self.client.auth.sign_in_with_password({
                    "email": email_or_phone,
                    "password": password
                })
                return {"success": True, "user": response.user, "session": response.session}
            else:
                # For phone number login, look up the email in user_profiles
                try:
                    phone_query = self.client.table("user_profiles").select("email").eq("phone_number", email_or_phone).execute()

                    if phone_query.data and len(phone_query.data) > 0:
                        user_email = phone_query.data[0]["email"]
                        response = self.client.auth.sign_in_with_password({
                            "email": user_email,
                            "password": password
                        })
                        return {"success": True, "user": response.user, "session": response.session}
                    else:
                        return {"success": False, "error": "Phone number not found. Please register as a new user or use your email address."}

                except Exception as lookup_error:
                    return {"success": False, "error": f"Error looking up phone number: {str(lookup_error)}"}

        except Exception as e:
            return {"success": False, "error": str(e)}

    def sign_out(self) -> Dict[str, Any]:
        """Sign out current user"""
        try:
            self.client.auth.sign_out()
            return {"success": True}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def update_password(self, new_password: str) -> Dict[str, Any]:
        """Update current user's password"""
        try:
            response = self.client.auth.update_user({
                "password": new_password
            })
            return {"success": True, "user": response.user}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def get_current_user(self) -> Optional[Dict[str, Any]]:
        """Get currently authenticated user"""
        try:
            user = self.client.auth.get_user()
            return user.user if user.user else None
        except:
            return None

    def create_user_profile(self, user_id: str, phone_number: str, email: str) -> Dict[str, Any]:
        """Create user profile record"""
        try:
            response = self.client.table("user_profiles").insert({
                "id": user_id,
                "phone_number": phone_number,
                "email": email
            }).execute()
            return {"success": True, "data": response.data}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def save_responses(self, user_id: str, responses: Dict[str, Any]) -> Dict[str, Any]:
        """Save user responses"""
        try:
            response_data = {
                "user_id": user_id,
                **responses
            }
            response = self.client.table("responses").insert(response_data).execute()
            return {"success": True, "data": response.data}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def get_user_responses(self, user_id: str) -> Dict[str, Any]:
        """Get user's current responses"""
        try:
            response = self.client.table("responses").select("*").eq("user_id", user_id).execute()
            return {"success": True, "data": response.data[0] if response.data else None}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def update_responses(self, user_id: str, responses: Dict[str, Any]) -> Dict[str, Any]:
        """Update user responses and create history record"""
        try:
            # First get current responses for history
            current = self.get_user_responses(user_id)
            if current["success"] and current["data"]:
                # Create history record
                history_data = {
                    "user_id": user_id,
                    "response_id": current["data"]["id"],
                    **{k: v for k, v in current["data"].items() if k.startswith(('h', 'w', 'p', 'f'))},
                    "valid_to": "NOW()",
                    "is_current": False
                }
                self.client.table("response_history").insert(history_data).execute()

            # Update current responses
            response = self.client.table("responses").update(responses).eq("user_id", user_id).execute()
            return {"success": True, "data": response.data}
        except Exception as e:
            return {"success": False, "error": str(e)}

# Global instance
supabase_client = SupabaseClient()