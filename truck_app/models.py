from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    def _create_user(self, phone_number, email=None, password=None, **extra_fields):
        """Create and save a User with the given Phonenumber and password."""
        if not phone_number:
            raise ValueError('The given phone number must be set')
        phone_number = str(phone_number)
        email = self.normalize_email(email)
        user = self.model(phone_number=phone_number, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, phone_number, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(phone_number, email, password, **extra_fields)

    def create_superuser(self, phone_number, email=None, password=None, **extra_fields):
        """Create and save a SuperUser with the given Phonenumber and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self._create_user(phone_number, email, password, **extra_fields)


# Add the new field in Auth User default table
class CustomUser(AbstractUser):
    username = None
    phone_number = models.CharField(_('phone number'), max_length=12, unique=True)
    # email = models.CharField(_('email'), max_length=50, unique=True, null=True, blank=True)

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()


class Register(models.Model):
    user_name = models.CharField(max_length=100)
    user_phone_number = models.CharField(max_length=12)
    user_email = models.CharField(max_length=255)
    password1 = models.CharField(max_length=50,null=True, blank=True)
    password2 = models.CharField(max_length=50,null=True, blank=True)
    terms_condition = models.BooleanField(default=False)
    privacy_policy = models.BooleanField(default=False)
    otp = models.CharField(max_length=50, null=True, blank=True)
    registered_datetime = models.DateTimeField()
    is_verified = models.BooleanField(null=True, blank=True)
    created = models.DateTimeField()
    updated = models.DateTimeField()


class UserProfile(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    user_name = models.CharField(max_length=100)
    user_phone_number = models.CharField(max_length=12)
    user_email = models.CharField(max_length=255)
    password = models.CharField(max_length=50)
    terms_condition = models.BooleanField(default=False)
    privacy_policy = models.BooleanField(default=False)
    user_created = models.DateTimeField()
    created = models.DateTimeField()
    updated = models.DateTimeField()


class HouseShiftingDetails(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    booking_id = models.CharField(max_length=100, null=True, blank=True)
    house_shifting_type = models.CharField(max_length=100, null=True, blank=True)
    shifting_type = models.CharField(max_length=100, null=True, blank=True)
    pickup_location = models.CharField(max_length=500, null=True, blank=True)
    moving_datetime = models.CharField(max_length=100, null=True, blank=True)
    pickup_address = models.CharField(max_length=500, null=True, blank=True)
    pickup_floor = models.CharField(max_length=50, null=True, blank=True)
    pickup_lift = models.CharField(max_length=50, null=True, blank=True)
    drop_location = models.CharField(max_length=500, null=True, blank=True)
    drop_address = models.CharField(max_length=500, null=True, blank=True)
    drop_floor = models.CharField(max_length=50, null=True, blank=True)
    drop_lift = models.CharField(max_length=50, null=True, blank=True)
    order_placed_datetime = models.DateTimeField(null=True, blank=True)
    completed = models.BooleanField(null=True, blank=True)
    completed_date = models.DateTimeField(null=True, blank=True)
    created = models.DateTimeField(null=True, blank=True)
    updated = models.DateTimeField(null=True, blank=True)


class HouseShiftingSelectedVehicle(models.Model):
    house_shifting_details = models.ForeignKey(HouseShiftingDetails, on_delete=models.CASCADE)
    vehicle_name = models.CharField(max_length=100, null=True, blank=True)
    vehicle_type = models.CharField(max_length=100, null=True, blank=True)
    vehicle_image = models.CharField(max_length=1100, null=True, blank=True)
    vehicle_amount = models.CharField(max_length=1100, null=True, blank=True)
    total_shifting_KMs = models.CharField(max_length=1100, null=True, blank=True)
    created = models.DateTimeField(null=True, blank=True)
    updated = models.DateTimeField(null=True, blank=True)


class HouseShiftingProducts(models.Model):
    house_shifting_details = models.ForeignKey(HouseShiftingDetails, on_delete=models.CASCADE)
    product_amount = models.CharField(max_length=100, null=True, blank=True)
    single_sofa = models.CharField(max_length=100, null=True, blank=True)
    double_sofa = models.CharField(max_length=100, null=True, blank=True)
    three_seater = models.CharField(max_length=100, null=True, blank=True)
    four_seater = models.CharField(max_length=100, null=True, blank=True)
    five_seater = models.CharField(max_length=100, null=True, blank=True)
    six_seater = models.CharField(max_length=100, null=True, blank=True)
    recliner = models.CharField(max_length=100, null=True, blank=True)
    single_bed_storage = models.CharField(max_length=100, null=True, blank=True)
    single_bed_dismantallable = models.CharField(max_length=100, null=True, blank=True)
    double_bed_storage = models.CharField(max_length=100, null=True, blank=True)
    double_bed_dismantallable = models.CharField(max_length=100, null=True, blank=True)
    bunk_dismantallabel = models.CharField(max_length=100, null=True, blank=True)
    folding_cot_dismantallabel = models.CharField(max_length=100, null=True, blank=True)
    single_mattress_foldable = models.CharField(max_length=100, null=True, blank=True)
    single_mattress_non_foldable = models.CharField(max_length=100, null=True, blank=True)
    double_mattress_foldable = models.CharField(max_length=100, null=True, blank=True)
    double_mattress_nonfoldable = models.CharField(max_length=100, null=True, blank=True)
    dining_table_chairs = models.CharField(max_length=100, null=True, blank=True)
    baby_chairs = models.CharField(max_length=100, null=True, blank=True)
    rocking_chair = models.CharField(max_length=100, null=True, blank=True)
    plastic_floding_chair = models.CharField(max_length=100, null=True, blank=True)
    office_chair = models.CharField(max_length=100, null=True, blank=True)
    bed_side_table = models.CharField(max_length=100, null=True, blank=True)
    dressing_table = models.CharField(max_length=100, null=True, blank=True)
    study_or_computer_table = models.CharField(max_length=100, null=True, blank=True)
    center_table = models.CharField(max_length=100, null=True, blank=True)
    dining_table = models.CharField(max_length=100, null=True, blank=True)
    tea_poy = models.CharField(max_length=100, null=True, blank=True)
    tv_stand = models.CharField(max_length=100, null=True, blank=True)
    book_self = models.CharField(max_length=100, null=True, blank=True)
    mirror = models.CharField(max_length=100, null=True, blank=True)
    shoe_rack = models.CharField(max_length=100, null=True, blank=True)
    mandir = models.CharField(max_length=100, null=True, blank=True)
    iron_trunk_chest = models.CharField(max_length=100, null=True, blank=True)
    tv_size_upto_20 = models.CharField(max_length=100, null=True, blank=True)
    tv_size_29to43 = models.CharField(max_length=100, null=True, blank=True)
    tv_size_49to55 = models.CharField(max_length=100, null=True, blank=True)
    tv_size_above55 = models.CharField(max_length=100, null=True, blank=True)
    home_theater = models.CharField(max_length=100, null=True, blank=True)
    ac_split = models.CharField(max_length=100, null=True, blank=True)
    ac_window = models.CharField(max_length=100, null=True, blank=True)
    cooler = models.CharField(max_length=100, null=True, blank=True)
    ceiling_fan = models.CharField(max_length=100, null=True, blank=True)
    table_fan = models.CharField(max_length=100, null=True, blank=True)
    exhaust_fan = models.CharField(max_length=100, null=True, blank=True)
    mini_fridge = models.CharField(max_length=100, null=True, blank=True)
    small_fridge = models.CharField(max_length=100, null=True, blank=True)
    medium_fridge = models.CharField(max_length=100, null=True, blank=True)
    large_fridge = models.CharField(max_length=100, null=True, blank=True)
    large_above450_ltrs_fridge = models.CharField(max_length=100, null=True, blank=True)
    washing_machine = models.CharField(max_length=100, null=True, blank=True)
    geyser = models.CharField(max_length=100, null=True, blank=True)
    bath_tub = models.CharField(max_length=100, null=True, blank=True)
    gas_stove = models.CharField(max_length=100, null=True, blank=True)
    water_purifier = models.CharField(max_length=100, null=True, blank=True)
    microwave_otg = models.CharField(max_length=100, null=True, blank=True)
    chimney = models.CharField(max_length=100, null=True, blank=True)
    dish_washer = models.CharField(max_length=100, null=True, blank=True)
    gas_cylinder = models.CharField(max_length=100, null=True, blank=True)
    sewing_mechine = models.CharField(max_length=100, null=True, blank=True)
    vaccum_cleaner = models.CharField(max_length=100, null=True, blank=True)
    lamp = models.CharField(max_length=100, null=True, blank=True)
    plants = models.CharField(max_length=100, null=True, blank=True)
    iron_board = models.CharField(max_length=100, null=True, blank=True)
    dish_antenna = models.CharField(max_length=100, null=True, blank=True)
    inverter_ups = models.CharField(max_length=100, null=True, blank=True)
    treadmill = models.CharField(max_length=100, null=True, blank=True)
    piano_guitar = models.CharField(max_length=100, null=True, blank=True)
    service_carton_box = models.CharField(max_length=100, null=True, blank=True)
    self_carton_box = models.CharField(max_length=100, null=True, blank=True)
    gunny_bags = models.CharField(max_length=100, null=True, blank=True)
    created = models.DateTimeField(null=True, blank=True)
    updated = models.DateTimeField(null=True, blank=True)


class VehicleShiftingDetails(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    booking_id = models.CharField(max_length=100, null=True, blank=True)
    shifting_type = models.CharField(max_length=100, null=True, blank=True)
    moving_datetime = models.CharField(max_length=100, null=True, blank=True)
    pickup_location = models.CharField(max_length=500, null=True, blank=True)
    pickup_address = models.CharField(max_length=500, null=True, blank=True)
    pickup_floor = models.CharField(max_length=50, null=True, blank=True)
    pickup_lift = models.CharField(max_length=50, null=True, blank=True)
    drop_location = models.CharField(max_length=500, null=True, blank=True)
    drop_address = models.CharField(max_length=500, null=True, blank=True)
    drop_floor = models.CharField(max_length=50, null=True, blank=True)
    drop_lift = models.CharField(max_length=50, null=True, blank=True)
    order_place_datetime = models.DateTimeField(null=True, blank=True)
    completed = models.BooleanField(null=True, blank=True)
    completed_date = models.DateTimeField(null=True, blank=True)
    created = models.DateTimeField(null=True, blank=True)
    updated = models.DateTimeField(null=True, blank=True)


class ChosenShiftingVehicle(models.Model):
    vehicle_shifting_details = models.ForeignKey(VehicleShiftingDetails, on_delete=models.CASCADE)
    vehicle_amount = models.CharField(max_length=100, null=True, blank=True)
    vehicle_name = models.CharField(max_length=100, null=True, blank=True)
    vehicle_model = models.CharField(max_length=100, null=True, blank=True)
    vehicle_image = models.CharField(max_length=100, null=True, blank=True)
    order_place_datetime = models.DateTimeField(null=True, blank=True)
    created = models.DateTimeField(null=True, blank=True)
    updated = models.DateTimeField(null=True, blank=True)


class WareHouseStorageDetails(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    booking_id = models.CharField(max_length=100, null=True, blank=True)
    shifting_type = models.CharField(max_length=100, null=True, blank=True)
    pickup_location = models.CharField(max_length=500, null=True, blank=True)
    moving_datetime = models.CharField(max_length=100, null=True, blank=True)
    pickup_address = models.CharField(max_length=500, null=True, blank=True)
    pickup_floor = models.CharField(max_length=50, null=True, blank=True)
    pickup_lift = models.CharField(max_length=50, null=True, blank=True)
    storing_days = models.CharField(max_length=50, null=True, blank=True)
    order_place_datetime = models.DateTimeField(null=True, blank=True)
    completed = models.BooleanField(null=True, blank=True)
    completed_date = models.DateTimeField(null=True, blank=True)
    created = models.DateTimeField(null=True, blank=True)
    updated = models.DateTimeField(null=True, blank=True)


class WareHouseSelectedVehicle(models.Model):
    warehouse_storage_detail = models.ForeignKey(WareHouseStorageDetails, on_delete=models.CASCADE)
    vehicle_name = models.CharField(max_length=100, null=True, blank=True)
    vehicle_type = models.CharField(max_length=100, null=True, blank=True)
    vehicle_image = models.CharField(max_length=1100, null=True, blank=True)
    created = models.DateTimeField(null=True, blank=True)
    updated = models.DateTimeField(null=True, blank=True)


class WareHouseStoringProducts(models.Model):
    warehouse_storage_detail = models.ForeignKey(WareHouseStorageDetails, on_delete=models.CASCADE)
    product_amount = models.CharField(max_length=100, null=True, blank=True)
    single_sofa = models.CharField(max_length=100, null=True, blank=True)
    double_sofa = models.CharField(max_length=100, null=True, blank=True)
    three_seater = models.CharField(max_length=100, null=True, blank=True)
    four_seater = models.CharField(max_length=100, null=True, blank=True)
    five_seater = models.CharField(max_length=100, null=True, blank=True)
    six_seater = models.CharField(max_length=100, null=True, blank=True)
    recliner = models.CharField(max_length=100, null=True, blank=True)
    single_bed_storage = models.CharField(max_length=100, null=True, blank=True)
    single_bed_dismantallable = models.CharField(max_length=100, null=True, blank=True)
    double_bed_storage = models.CharField(max_length=100, null=True, blank=True)
    double_bed_dismantallable = models.CharField(max_length=100, null=True, blank=True)
    bunk_dismantallabel = models.CharField(max_length=100, null=True, blank=True)
    folding_cot_dismantallabel = models.CharField(max_length=100, null=True, blank=True)
    single_mattress_foldable = models.CharField(max_length=100, null=True, blank=True)
    single_mattress_non_foldable = models.CharField(max_length=100, null=True, blank=True)
    double_mattress_foldable = models.CharField(max_length=100, null=True, blank=True)
    double_mattress_nonfoldable = models.CharField(max_length=100, null=True, blank=True)
    dining_table_chairs = models.CharField(max_length=100, null=True, blank=True)
    baby_chairs = models.CharField(max_length=100, null=True, blank=True)
    rocking_chair = models.CharField(max_length=100, null=True, blank=True)
    plastic_floding_chair = models.CharField(max_length=100, null=True, blank=True)
    office_chair = models.CharField(max_length=100, null=True, blank=True)
    bed_side_table = models.CharField(max_length=100, null=True, blank=True)
    dressing_table = models.CharField(max_length=100, null=True, blank=True)
    study_or_computer_table = models.CharField(max_length=100, null=True, blank=True)
    center_table = models.CharField(max_length=100, null=True, blank=True)
    dining_table = models.CharField(max_length=100, null=True, blank=True)
    tea_poy = models.CharField(max_length=100, null=True, blank=True)
    tv_stand = models.CharField(max_length=100, null=True, blank=True)
    book_self = models.CharField(max_length=100, null=True, blank=True)
    mirror = models.CharField(max_length=100, null=True, blank=True)
    shoe_rack = models.CharField(max_length=100, null=True, blank=True)
    mandir = models.CharField(max_length=100, null=True, blank=True)
    iron_trunk_chest = models.CharField(max_length=100, null=True, blank=True)
    tv_size_upto_20 = models.CharField(max_length=100, null=True, blank=True)
    tv_size_29to43 = models.CharField(max_length=100, null=True, blank=True)
    tv_size_49to55 = models.CharField(max_length=100, null=True, blank=True)
    tv_size_above55 = models.CharField(max_length=100, null=True, blank=True)
    home_theater = models.CharField(max_length=100, null=True, blank=True)
    ac_split = models.CharField(max_length=100, null=True, blank=True)
    ac_window = models.CharField(max_length=100, null=True, blank=True)
    cooler = models.CharField(max_length=100, null=True, blank=True)
    ceiling_fan = models.CharField(max_length=100, null=True, blank=True)
    table_fan = models.CharField(max_length=100, null=True, blank=True)
    exhaust_fan = models.CharField(max_length=100, null=True, blank=True)
    mini_fridge = models.CharField(max_length=100, null=True, blank=True)
    small_fridge = models.CharField(max_length=100, null=True, blank=True)
    medium_fridge = models.CharField(max_length=100, null=True, blank=True)
    large_fridge = models.CharField(max_length=100, null=True, blank=True)
    large_above450_ltrs_fridge = models.CharField(max_length=100, null=True, blank=True)
    washing_machine = models.CharField(max_length=100, null=True, blank=True)
    geyser = models.CharField(max_length=100, null=True, blank=True)
    bath_tub = models.CharField(max_length=100, null=True, blank=True)
    gas_stove = models.CharField(max_length=100, null=True, blank=True)
    water_purifier = models.CharField(max_length=100, null=True, blank=True)
    microwave_otg = models.CharField(max_length=100, null=True, blank=True)
    chimney = models.CharField(max_length=100, null=True, blank=True)
    dish_washer = models.CharField(max_length=100, null=True, blank=True)
    gas_cylinder = models.CharField(max_length=100, null=True, blank=True)
    sewing_mechine = models.CharField(max_length=100, null=True, blank=True)
    vaccum_cleaner = models.CharField(max_length=100, null=True, blank=True)
    lamp = models.CharField(max_length=100, null=True, blank=True)
    plants = models.CharField(max_length=100, null=True, blank=True)
    iron_board = models.CharField(max_length=100, null=True, blank=True)
    dish_antenna = models.CharField(max_length=100, null=True, blank=True)
    inverter_ups = models.CharField(max_length=100, null=True, blank=True)
    treadmill = models.CharField(max_length=100, null=True, blank=True)
    piano_guitar = models.CharField(max_length=100, null=True, blank=True)
    service_carton_box = models.CharField(max_length=100, null=True, blank=True)
    self_carton_box = models.CharField(max_length=100, null=True, blank=True)
    gunny_bags = models.CharField(max_length=100, null=True, blank=True)
    created = models.DateTimeField(null=True, blank=True)
    updated = models.DateTimeField(null=True, blank=True)
    selected = models.DateTimeField(null=True, blank=True)


class OrderBooking(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    booking_id = models.CharField(max_length=100, null=True, blank=True)
    house_shifting_details_id = models.CharField(max_length=100, null=True, blank=True)
    house_shifting_product_id = models.CharField(max_length=100, null=True, blank=True)
    vehicle_shifting_details_id = models.CharField(max_length=100, null=True, blank=True)
    chosen_shifting_vehicle_details_id = models.CharField(max_length=100, null=True, blank=True)
    ware_house_storing_details_id = models.CharField(max_length=100, null=True, blank=True)
    ware_house_storing_products_id = models.CharField(max_length=100, null=True, blank=True)
    booking_datetime = models.CharField(max_length=100, null=True, blank=True)
    shifting_type = models.CharField(max_length=100, null=True, blank=True)
    payment_method = models.CharField(max_length=100, null=True, blank=True)
    total_amount = models.CharField(max_length=100, null=True, blank=True)
    created = models.DateTimeField(null=True, blank=True)
    updated = models.DateTimeField(null=True, blank=True)
