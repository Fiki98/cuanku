from dotenv import load_dotenv

load_dotenv() 

import sys
from app.menus.util import clear_screen, pause
from app.client.engsel import *
from app.menus.payment import show_transaction_history
from app.service.auth import AuthInstance
from app.menus.bookmark import show_bookmark_menu
from app.menus.account import show_account_menu
from app.menus.package import fetch_my_packages, get_packages_by_family
from app.menus.hot import show_hot_menu, show_hot_menu2
from app.service.sentry import enter_sentry_mode
from app.menus.purchase import purchase_by_family, purchase_loop
from app.util import save_api_key
from app.menus.family_bookmark import show_family_bookmark_menu

def show_main_menu(active_user):
    clear_screen()
    print(f"Active Number: {active_user['number']}")
    print("-------------------------------------------------------")
    print("Menu:")
    print("1. Login/Ganti akun")
    print("2. Lihat Paket Saya")
    print("3. Beli Paket 🔥 HOT 🔥")
    print("4. Beli Paket 🔥 HOT-2 🔥")
    print("5. Riwayat Transaksi")
    print("6. Beli Paket Berdasarkan Family Code")
    print("7. [Test] Purchase all packages in family code")
    print("8. Mode Custom (family code dan nomer order)")
    print("-------------------------------------------------------")
    print("9. Bookmark Family Code")
    print("10. Ganti API Key")
    print("99. Tutup aplikasi")
    print("-------------------------------------------------------")

show_menu = True
def main():
    
    while True:
        active_user = AuthInstance.get_active_user()

        # Logged in
        if active_user is not None:
            show_main_menu(active_user)

            choice = input("Pilih menu: ")
            if choice == "1":
                selected_user_number = show_account_menu()
                if selected_user_number:
                    AuthInstance.set_active_user(selected_user_number)
                else:
                    print("No user selected or failed to load user.")
                continue
            elif choice == "2":
                fetch_my_packages()
                continue
            elif choice == "3":
                show_hot_menu()
            elif choice == "4":
                show_hot_menu2()
            elif choice == "5":
                show_transaction_history(AuthInstance.api_key, active_user["tokens"])
            elif choice == "6":
                family_code = input("Enter family code (or '99' to cancel): ")
                if family_code == "99":
                    continue
                get_packages_by_family(family_code)
            elif choice == "7":
                family_code = input("Enter family code (or '99' to cancel): ")
                if family_code == "99":
                    continue
                use_decoy = input("Use decoy package? (y/n): ").lower() == 'y'
                pause_on_success = input("Aktifkan mode pause? (y/n): ").lower() == 'y'
                purchase_by_family(family_code, use_decoy, pause_on_success)
            elif choice == "8":
                family_code = input("Enter family code: ")
                order = int(input("Enter order number: "))
                delay = int(input("Enter delay in seconds: "))
                while True:
                    if not purchase_loop(
                        family_code=family_code,
                        order=order,
                        use_decoy=True,
                        delay=delay,
                        pause_on_success=True
                    ):
                        break
            elif choice == "9":
                show_family_bookmark_menu()
            elif choice == "10":
                new_api_key = input("Masukkan API key baru: ").strip()
                if new_api_key:
                    save_api_key(new_api_key)
                    AuthInstance.api_key = new_api_key
                    print("API key berhasil diperbarui.")
                else:
                    print("API key tidak boleh kosong.")
                pause()
            elif choice == "99":
                print("Exiting the application.")
                sys.exit(0)
            else:
                print("Invalid choice. Please try again.")
                pause()
        else:
            # Not logged in
            selected_user_number = show_account_menu()
            if selected_user_number:
                AuthInstance.set_active_user(selected_user_number)
            else:
                print("No user selected or failed to load user.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nExiting the application.")
    # except Exception as e:
    #     print(f"An error occurred: {e}")
