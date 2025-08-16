# Simple POS Automation Testing (Final Project QA)

Automation testing menggunakan **Selenium + Pytest** untuk menguji fitur utama pada aplikasi **Simple POS**  
Link Aplikasi: [https://simple-pos-pwdk.netlify.app/](https://simple-pos-pwdk.netlify.app/)

---

## 📌 Test Scope

### 1. **Authentication**

- **Login** dengan kredensial valid.
- **Login gagal** (invalid email/password).

### 2. **Point of Sale (POS)**

- **Search Product** berdasarkan nama produk dan
- **Filter Category** (misalnya Electronics, Clothing, Books, dll).
- **Add to Cart**.
- **Decrease Quantity**.
- **Increase Quantity**.
- **Remove Product** dari cart.
- **Checkout** dengan input customer info.
- **Select Payment Method**.
- **Complete Transaction**.

### 3. **Reports**

- Akses halaman **Reports** dari sidebar.

## 🧪 Optional Tests

Fitur di bawah ini **tidak termasuk scope utama**, namun dibuat untuk latihan tambahan.

### Transactions Page

- **View Transactions**: Membuka halaman Transactions.
- **Filter by Time**: All Time, Today, Last 7 Days, Last 30 Days.
- **Search by Transaction ID**.
- Validasi jika **data kosong** → tampil pesan *"No transactions found"*.

⚠ **Catatan**:  
Data transaksi pada aplikasi ini hanya disimpan di **localStorage**.  
Jika automation dijalankan pada browser baru, data transaksi sebelumnya tidak akan muncul.  
Karena itu, test ini dibuat **opsional** (`@pytest.mark.optional`) dan tidak mempengaruhi scope utama.

---


- Login


Valid Login (Automation) ✅

Invalid Login – wrong password (Automation) ✅

Invalid Login – email without @ (Manual)

Invalid Login – empty password (Manual)

Invalid Login – empty email (Manual)

🛒 Product Search & Selection

Search product with valid name and selection (Automation) ✅

Search product with invalid name (Automation) ✅

Search product with case insensitive and selection (Automation) ✅

Search product with partial keyword (e.g. "Coff") and selection (Automation) ✅

Search product with full name and selection (Automation) ✅

Search product with category filter and selection (Automation) ✅

Search product with empty search → show all products (Automation) ✅

Search product with invalid name → no selection allowed (Automation) ✅

🛍️ Cart Management

Add single product to cart (Automation) ✅

Increase product quantity in cart (Automation) ✅

Decrease product quantity in cart (Automation) ✅

Remove product from cart (Automation) ✅

Validate cart empty state (Automation) ✅

Try to increase quantity beyond available stock (Automation – Negative) ✅

Ensure total price updates correctly after add/remove/update (Automation) ✅

💳 Checkout & Payment Simulation

Checkout with Cash payment (Automation) ✅

Checkout with Card payment (Automation) ✅

Attempt checkout with empty cart (Automation – Negative) ✅

Validate success message / receipt displayed after checkout (Automation) ✅

📊 Reports

Open Reports page after transactions (Automation) ✅

Verify transaction appears in report list (Automation) ✅

Validate report fields (date, total, payment method) are correct (Automation) ✅

🚪 Logout

Logout from POS system (Automation) ✅

Verify user redirected to login page (Automation) ✅

Try accessing POS page after logout → should redirect to login (Automation – Negative) ✅




