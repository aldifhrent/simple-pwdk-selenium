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
