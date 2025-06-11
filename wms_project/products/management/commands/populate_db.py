from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta, date
import random
from decimal import Decimal

from products.models import Category, Product
from orders.models import Customer, Order, OrderItem
from suppliers.models import Supplier, Restock
from inventory.models import StockMovement
from authentication.models import UserProfile

class Command(BaseCommand):
    help = 'Ma\'lumotlar bazasini namunaviy ma\'lumotlar bilan to\'ldiradi'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Ma\'lumotlar bazasini to\'ldirish boshlandi...'))
        
        # Admin foydalanuvchi yaratish
        self.create_admin_user()
        
        # Kategoriyalar yaratish
        self.create_categories()
        
        # Mahsulotlar yaratish
        self.create_products()
        
        # Mijozlar yaratish
        self.create_customers()
        
        # Ta'minotchilar yaratish
        self.create_suppliers()
        
        # Buyurtmalar yaratish
        self.create_orders()
        
        # Ta'minot buyurtmalari yaratish
        self.create_restocks()
        
        # Inventar harakatlari yaratish
        self.create_stock_movements()
        
        self.stdout.write(self.style.SUCCESS('Ma\'lumotlar bazasi muvaffaqiyatli to\'ldirildi!'))

    def create_admin_user(self):
        if not User.objects.filter(username='admin').exists():
            admin_user = User.objects.create_superuser(
                username='admin',
                email='admin@wms.uz',
                password='admin123',
                first_name='Administrator',
                last_name='WMS'
            )
            
            # Admin uchun profil yaratish
            UserProfile.objects.create(
                user=admin_user,
                phone='+998712345678',
                address='Toshkent sh., Amir Temur ko\'ch., 1-uy',
                position='Tizim administratori'
            )
            
            self.stdout.write(self.style.SUCCESS('Admin foydalanuvchi yaratildi: admin/admin123'))

    def create_categories(self):
        categories_data = [
            {'name': 'Erkaklar kiyimi', 'description': 'Erkaklar uchun kiyim-kechak'},
            {'name': 'Ayollar kiyimi', 'description': 'Ayollar uchun kiyim-kechak'},
            {'name': 'Bolalar kiyimi', 'description': 'Bolalar uchun kiyim-kechak'},
            {'name': 'Poyabzal', 'description': 'Har xil turdagi poyabzallar'},
            {'name': 'Aksessuarlar', 'description': 'Kiyim aksessuarlari'},
            {'name': 'Sport kiyimi', 'description': 'Sport va faol hayot uchun kiyimlar'},
            {'name': 'Ichki kiyim', 'description': 'Ichki kiyim va uyqu kiyimlari'},
        ]
        
        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                name=cat_data['name'],
                defaults={'description': cat_data['description']}
            )
            if created:
                self.stdout.write(f'Kategoriya yaratildi: {category.name}')

    def create_products(self):
        categories = Category.objects.all()
        sizes = ['XS', 'S', 'M', 'L', 'XL', 'XXL']
        colors = ['Qora', 'Oq', 'Ko\'k', 'Qizil', 'Yashil', 'Sariq', 'Pushti', 'Kulrang', 'Jigarrang']
        
        products_data = [
            # Erkaklar kiyimi
            {'name': 'Klassik ko\'ylak', 'category': 'Erkaklar kiyimi', 'price_range': (50, 150)},
            {'name': 'Jins shim', 'category': 'Erkaklar kiyimi', 'price_range': (80, 200)},
            {'name': 'Polo ko\'ylak', 'category': 'Erkaklar kiyimi', 'price_range': (40, 120)},
            {'name': 'Kostyum', 'category': 'Erkaklar kiyimi', 'price_range': (300, 800)},
            {'name': 'Futbolka', 'category': 'Erkaklar kiyimi', 'price_range': (20, 60)},
            {'name': 'Sviter', 'category': 'Erkaklar kiyimi', 'price_range': (70, 180)},
            
            # Ayollar kiyimi
            {'name': 'Bluzka', 'category': 'Ayollar kiyimi', 'price_range': (45, 130)},
            {'name': 'Ko\'ylak', 'category': 'Ayollar kiyimi', 'price_range': (70, 250)},
            {'name': 'Yubka', 'category': 'Ayollar kiyimi', 'price_range': (50, 150)},
            {'name': 'Jins shim', 'category': 'Ayollar kiyimi', 'price_range': (90, 220)},
            {'name': 'Kardigon', 'category': 'Ayollar kiyimi', 'price_range': (60, 180)},
            {'name': 'Tunika', 'category': 'Ayollar kiyimi', 'price_range': (55, 140)},
            
            # Bolalar kiyimi
            {'name': 'Bolalar futbolkasi', 'category': 'Bolalar kiyimi', 'price_range': (15, 40)},
            {'name': 'Bolalar jins shimi', 'category': 'Bolalar kiyimi', 'price_range': (35, 80)},
            {'name': 'Bolalar ko\'ylagi', 'category': 'Bolalar kiyimi', 'price_range': (25, 70)},
            {'name': 'Bolalar sviter', 'category': 'Bolalar kiyimi', 'price_range': (30, 65)},
            
            # Poyabzal
            {'name': 'Klassik tufli', 'category': 'Poyabzal', 'price_range': (100, 300)},
            {'name': 'Krossovka', 'category': 'Poyabzal', 'price_range': (80, 250)},
            {'name': 'Sandal', 'category': 'Poyabzal', 'price_range': (40, 120)},
            {'name': 'Bot', 'category': 'Poyabzal', 'price_range': (120, 350)},
            
            # Aksessuarlar
            {'name': 'Kamar', 'category': 'Aksessuarlar', 'price_range': (25, 80)},
            {'name': 'Shlyapa', 'category': 'Aksessuarlar', 'price_range': (30, 100)},
            {'name': 'Qo\'lqop', 'category': 'Aksessuarlar', 'price_range': (15, 50)},
            {'name': 'Sharf', 'category': 'Aksessuarlar', 'price_range': (20, 70)},
            
            # Sport kiyimi
            {'name': 'Sport kostyumi', 'category': 'Sport kiyimi', 'price_range': (80, 200)},
            {'name': 'Yoga taytsi', 'category': 'Sport kiyimi', 'price_range': (40, 100)},
            {'name': 'Sport futbolka', 'category': 'Sport kiyimi', 'price_range': (25, 70)},
            {'name': 'Sport shorti', 'category': 'Sport kiyimi', 'price_range': (30, 80)},
            
            # Ichki kiyim
            {'name': 'Ichki ko\'ylak', 'category': 'Ichki kiyim', 'price_range': (15, 45)},
            {'name': 'Uyqu kiyimi', 'category': 'Ichki kiyim', 'price_range': (40, 120)},
            {'name': 'Paypoq', 'category': 'Ichki kiyim', 'price_range': (5, 25)},
        ]
        
        for product_data in products_data:
            category = categories.filter(name=product_data['category']).first()
            if category:
                for i in range(random.randint(2, 4)):  # Har bir mahsulotdan 2-4 ta variant
                    size = random.choice(sizes)
                    color = random.choice(colors)
                    price = Decimal(random.uniform(*product_data['price_range']))
                    quantity = random.randint(10, 100)
                    
                    product_name = f"{product_data['name']} ({color}, {size})"
                    
                    product, created = Product.objects.get_or_create(
                        name=product_name,
                        category=category,
                        size=size,
                        color=color,
                        defaults={
                            'description': f"{product_data['name']} - {color} rangda, {size} o'lchamda",
                            'price': price,
                            'quantity': quantity,
                            'low_stock_threshold': random.randint(5, 15)
                        }
                    )
                    if created:
                        self.stdout.write(f'Mahsulot yaratildi: {product.name}')

    def create_customers(self):
        customers_data = [
            {'name': 'Akmal Karimov', 'email': 'akmal@email.com', 'phone': '+998901234567', 'address': 'Toshkent sh., Yunusobod t., 1-uy'},
            {'name': 'Dilnoza Rahimova', 'email': 'dilnoza@email.com', 'phone': '+998902345678', 'address': 'Toshkent sh., Chilonzor t., 25-uy'},
            {'name': 'Bobur Aliyev', 'email': 'bobur@email.com', 'phone': '+998903456789', 'address': 'Samarqand sh., Registon ko\'ch., 10-uy'},
            {'name': 'Malika Tosheva', 'email': 'malika@email.com', 'phone': '+998904567890', 'address': 'Buxoro sh., Mustaqillik ko\'ch., 5-uy'},
            {'name': 'Jasur Nazarov', 'email': 'jasur@email.com', 'phone': '+998905678901', 'address': 'Andijon sh., Navoi ko\'ch., 15-uy'},
            {'name': 'Sevara Yusupova', 'email': 'sevara@email.com', 'phone': '+998906789012', 'address': 'Namangan sh., Uchtepa t., 8-uy'},
            {'name': 'Otabek Saidov', 'email': 'otabek@email.com', 'phone': '+998907890123', 'address': 'Farg\'ona sh., Margilon ko\'ch., 20-uy'},
            {'name': 'Nigora Abdullayeva', 'email': 'nigora@email.com', 'phone': '+998908901234', 'address': 'Qarshi sh., Nasaf ko\'ch., 12-uy'},
            {'name': 'Sardor Mirzayev', 'email': 'sardor@email.com', 'phone': '+998909012345', 'address': 'Nukus sh., Amir Temur ko\'ch., 7-uy'},
            {'name': 'Gulnora Hasanova', 'email': 'gulnora@email.com', 'phone': '+998900123456', 'address': 'Urganch sh., Al-Xorazmiy ko\'ch., 18-uy'},
            {'name': 'Aziz Tursunov', 'email': 'aziz@email.com', 'phone': '+998911234567', 'address': 'Toshkent sh., Mirzo Ulug\'bek t., 33-uy'},
            {'name': 'Feruza Qodirova', 'email': 'feruza@email.com', 'phone': '+998912345678', 'address': 'Samarqand sh., Amir Temur ko\'ch., 45-uy'},
        ]
        
        for customer_data in customers_data:
            customer, created = Customer.objects.get_or_create(
                email=customer_data['email'],
                defaults={
                    'name': customer_data['name'],
                    'phone': customer_data['phone'],
                    'address': customer_data['address']
                }
            )
            if created:
                self.stdout.write(f'Mijoz yaratildi: {customer.name}')

    def create_suppliers(self):
        suppliers_data = [
            {
                'name': 'Toshkent Tekstil',
                'contact_person': 'Aziz Karimov',
                'email': 'info@toshkenttekstil.uz',
                'phone': '+998712345678',
                'address': 'Toshkent sh., Sergeli t., Tekstil ko\'ch., 45-uy'
            },
            {
                'name': 'Marg\'ilon Ipak',
                'contact_person': 'Dilshod Rahmonov',
                'email': 'sales@margilon-silk.uz',
                'phone': '+998732456789',
                'address': 'Marg\'ilon sh., Ipak yo\'li, 12-uy'
            },
            {
                'name': 'Buxoro Fashion',
                'contact_person': 'Madina Tosheva',
                'email': 'orders@buxorofashion.uz',
                'phone': '+998652567890',
                'address': 'Buxoro sh., Hunarmandchilik ko\'ch., 8-uy'
            },
            {
                'name': 'Samarqand Style',
                'contact_person': 'Jamshid Aliyev',
                'email': 'contact@samarqandstyle.uz',
                'phone': '+998662678901',
                'address': 'Samarqand sh., Registon maydoni, 3-uy'
            },
            {
                'name': 'Andijon Poyabzal',
                'contact_person': 'Nodira Yusupova',
                'email': 'info@andijonshoes.uz',
                'phone': '+998742789012',
                'address': 'Andijon sh., Hunarmandlar ko\'ch., 22-uy'
            },
            {
                'name': 'Namangan Tekstil',
                'contact_person': 'Sherzod Olimov',
                'email': 'info@namangantextile.uz',
                'phone': '+998692123456',
                'address': 'Namangan sh., Sanoat ko\'ch., 15-uy'
            }
        ]
        
        for supplier_data in suppliers_data:
            supplier, created = Supplier.objects.get_or_create(
                name=supplier_data['name'],
                defaults={
                    'contact_person': supplier_data['contact_person'],
                    'email': supplier_data['email'],
                    'phone': supplier_data['phone'],
                    'address': supplier_data['address']
                }
            )
            if created:
                # Ta'minotchiga mahsulotlar biriktirish
                products = Product.objects.order_by('?')[:random.randint(8, 20)]
                supplier.products.set(products)
                self.stdout.write(f'Ta\'minotchi yaratildi: {supplier.name}')

    def create_orders(self):
        customers = Customer.objects.all()
        products = Product.objects.all()
        statuses = ['RECEIVED', 'PROCESSING', 'SHIPPED', 'DELIVERED', 'CANCELLED']
        
        for i in range(60):  # 60 ta buyurtma yaratish
            customer = random.choice(customers)
            status = random.choice(statuses)
            
            # Buyurtma sanasini oxirgi 45 kun ichida tasodifiy tanlash
            days_ago = random.randint(0, 45)
            order_date = timezone.now() - timedelta(days=days_ago)
            
            order = Order.objects.create(
                customer=customer,
                status=status,
                total_amount=Decimal('0'),  # Keyinroq hisoblanadi
                notes=f"Buyurtma #{i+1} - {customer.name} uchun"
            )
            order.created_at = order_date
            order.save()
            
            # Buyurtma elementlari yaratish
            num_items = random.randint(1, 6)
            total_amount = Decimal('0')
            
            selected_products = random.sample(list(products), min(num_items, len(products)))
            
            for product in selected_products:
                quantity = random.randint(1, 4)
                price = product.price
                
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=quantity,
                    price=price
                )
                
                total_amount += price * quantity
            
            order.total_amount = total_amount
            order.save()
            
            self.stdout.write(f'Buyurtma yaratildi: {order.order_number}')

    def create_restocks(self):
        suppliers = Supplier.objects.all()
        statuses = ['PENDING', 'ORDERED', 'RECEIVED', 'CANCELLED']
        
        for i in range(40):  # 40 ta ta'minot buyurtmasi yaratish
            supplier = random.choice(suppliers)
            status = random.choice(statuses)
            
            # Ta'minotchi mahsulotlaridan birini tanlash
            supplier_products = supplier.products.all()
            if supplier_products:
                product = random.choice(supplier_products)
                quantity = random.randint(20, 200)
                
                # Kutilayotgan sana
                days_ahead = random.randint(5, 30)
                expected_date = date.today() + timedelta(days=days_ahead)
                
                restock = Restock.objects.create(
                    supplier=supplier,
                    product=product,
                    quantity=quantity,
                    status=status,
                    expected_date=expected_date,
                    notes=f"Ta'minot #{i+1} - {product.name} uchun {quantity} dona"
                )
                
                # Sanani o'tgan kunlarga o'rnatish
                days_ago = random.randint(0, 60)
                restock_date = timezone.now() - timedelta(days=days_ago)
                restock.created_at = restock_date
                restock.save()
                
                self.stdout.write(f'Ta\'minot buyurtmasi yaratildi: {restock}')

    def create_stock_movements(self):
        products = Product.objects.all()
        admin_user = User.objects.filter(is_superuser=True).first()
        movement_types = ['IN', 'OUT']
        reasons = [
            'Yangi mahsulot qabuli',
            'Sotuvdan qaytarish',
            'Inventarizatsiya',
            'Buzilgan mahsulot',
            'Sotish',
            'Namuna uchun',
            'Aksiya uchun',
            'Transfer',
            'Qaytarish',
            'Tekshirish'
        ]
        
        for i in range(150):  # 150 ta inventar harakati yaratish
            product = random.choice(products)
            movement_type = random.choice(movement_types)
            quantity = random.randint(1, 25)
            reason = random.choice(reasons)
            
            # Harakat sanasini oxirgi 90 kun ichida tasodifiy tanlash
            days_ago = random.randint(0, 90)
            movement_date = timezone.now() - timedelta(days=days_ago)
            
            # Mahsulot miqdorini tekshirish (chiqim uchun)
            if movement_type == 'OUT' and product.quantity < quantity:
                quantity = max(1, min(quantity, product.quantity))
            
            # StockMovement yaratishdan oldin mahsulot miqdorini saqlab qo'yamiz
            original_quantity = product.quantity
            
            movement = StockMovement.objects.create(
                product=product,
                quantity=quantity,
                movement_type=movement_type,
                reason=reason,
                staff=admin_user
            )
            movement.created_at = movement_date
            movement.save()
            
            self.stdout.write(f'Inventar harakati yaratildi: {movement}')
