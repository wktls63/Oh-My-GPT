from django.db                      import models
from django.contrib.auth.models     import BaseUserManager, AbstractBaseUser

import uuid


class UserManager(BaseUserManager):

    # 일반 유저 생성
    def create_user(self, email, password=None):

        # 이메일 값이 없으면 에러 : 당신은 이메일이 필요합니다.
        if not email:
            raise ValueError("Users must have an email address")
        
        # 비밀번호 값이 없으면 에러 : 당신은 비밀번호가 필요합니다.   
        if not password:
            raise ValueError("Users must have a password")
        
        # 이메일 양식이 맞는지 확인
        email = self.normalize_email(email)
        user = self.model(
            email=email,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    # 어드민 유저 생성
    def create_superuser(self, email, password=None):
        user = self.create_user(email=email, password=password)
        user.is_staff = True
        user.save(using=self._db)
        return user


class User (AbstractBaseUser):
    """
    사용자 정보에 대한 모델 
    """

    email                               = models.EmailField(verbose_name = "이메일", max_length = 100, unique = True)
    password                            = models.CharField(verbose_name = "비밀번호")

    PAYMENT_BASIC       = 0
    PAYMENT_PRO         = 1
    PAYMENT_PRO_PLUS    = 2
    PAYMENT_ENTERPRISE  = 3

    # 구독중인 아이템
    PAYMENT_CHOICES     = [
                            (PAYMENT_BASIC, "무료"),
                            (PAYMENT_PRO, "프로"),
                            (PAYMENT_PRO_PLUS, "프로플러스"),
                            (PAYMENT_ENTERPRISE, "엔터프라이즈")
                          ]             


    payment_status                      = models.IntegerField(verbose_name = "결제 상태", choices = PAYMENT_CHOICES, default = PAYMENT_BASIC)
    registered_date                     = models.DateTimeField(verbose_name = "가입일", auto_now = True)
    
    is_active                           = models.BooleanField(default = True)
    is_staff                            = models.BooleanField(default = False)

    USERNAME_FIELD                      = "email"
    REQUIRED_FIELDS                     = ["password"]

    # 헬퍼 클래스
    objects                             = UserManager()

    def has_perm(self, perm, obj=None):
        return self.is_staff

    def has_module_perms(self, app_label):
        return self.is_staff

    def __str__(self):
        return f"{self.email}"

    class Meta:
        verbose_name            = '유저'
        verbose_name_plural     = '유저 목록'


class Posting(models.Model):
    """
    고객센터 포스팅에 대한 모델 
    """

    user_id                             = models.ForeignKey(User, verbose_name = "유저 아이디", on_delete = models.CASCADE)
    title                               = models.CharField(verbose_name = "제목", max_length = 50)
    content                             = models.TextField(verbose_name = "내용")
    created_date                        = models.DateTimeField(verbose_name = "게시일", auto_now_add = True)
    views                               = models.IntegerField(verbose_name = "조회수", default = 0)

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name            = '포스팅'
        verbose_name_plural     = '포스팅 목록'


class Data(models.Model):
    file_dir                            = models.TextField(verbose_name = "데이터 경로")

    def __str__(self):
        return f"{self.file_dir}"

    class Meta:
        verbose_name            = '데이터 경로'
        verbose_name_plural     = '데이터 경로 목록'


class AIModel(models.Model):
    """
    AI모델에 대한 모델 
    """
    model_id                            = models.UUIDField(primary_key=True, verbose_name = "모델 id", default = uuid.uuid4, editable = False)
    user_id                             = models.ForeignKey(User, verbose_name = "유저 id", on_delete = models.CASCADE)
    data_id                             = models.ForeignKey(Data, verbose_name = "모델 데이터 id", on_delete = models.CASCADE)
    model_name                          = models.CharField(verbose_name = "모델 이름", max_length = 50)
    create_date                         = models.DateTimeField(verbose_name = "생성일", null = True)

    def __str__(self):
        return f"{self.model_name}"

    class Meta:
        verbose_name            = 'AI모델'
        verbose_name_plural     = 'AI모델 목록'


class ChatRoom(models.Model):
    """
    채팅방에 대한 모델 
    """

    user_id                             = models.ForeignKey(User, verbose_name = "유저 id", on_delete = models.CASCADE)
    model_id                            = models.ForeignKey(AIModel, verbose_name = "모델 id", on_delete = models.CASCADE, )
    
    last_message                        = models.CharField(verbose_name = "마지막 메세지", default = "대화를 시작해보세요!")

    def __str__(self):
        return f"{self.last_message}"

    class Meta:
        verbose_name            = '채팅방'
        verbose_name_plural     = '채팅방 목록'


class Message(models.Model):
    """
    채팅 메세지에 대한 모델
    """

    chat_id                             = models.ForeignKey(ChatRoom, verbose_name = "채팅방 id", on_delete = models.CASCADE)
    sender_id                           = models.ForeignKey(User, verbose_name = "채팅방 id", on_delete = models.CASCADE, null = True, blank = True)
    content                             = models.TextField(verbose_name = "메세지")
    send_date                           = models.DateTimeField(verbose_name = "발송일시", auto_now = True)

    is_user                             = models.BooleanField(verbose_name = "사용자가 보낸 메세지 인지", default = True)

    def __str__(self):
        return f"{self.content}"

    class Meta:
        verbose_name            = '채팅 메세지'
        verbose_name_plural     = '채팅 메세지 목록'


class SubscriptionProduct(models.Model):
    item_name                           = models.CharField(verbose_name = "상품명")
    amount                              = models.IntegerField(verbose_name = "상품 가격", default = 0)

    def str(self):
        return f"{self.item_name}"

    class Meta:
        verbose_name            = '상품'
        verbose_name_plural     = '상품 목록'


class Payment(models.Model):
    user_id                             = models.ForeignKey(User, verbose_name = "유저 id", on_delete = models.CASCADE)
    subscription_product_id              = models.ForeignKey(SubscriptionProduct, verbose_name = "상품ID", on_delete = models.CASCADE, default="")
    merchant_id                         = models.UUIDField(verbose_name = "가맹점 코드", default = uuid.uuid4, editable = False)
    amount                              = models.PositiveIntegerField(verbose_name='결제 금액', default=100)
    payment_date                        = models.DateTimeField(verbose_name = "결제 갱신일", auto_now_add = True)

    PAYMENT_TYPE_CHOICES                = [('card', '신용카드')]
    payment_type                        = models.CharField(verbose_name='결제 수단', max_length=10, choices=PAYMENT_TYPE_CHOICES, default='card')

    STATUS_CHOICES                      =   [
                                            ('await', '결제대기'),
                                            ('paid', '결제성공'),
                                            ('failed', '결제실패'),
                                            ('cancelled', '결제취소')
                                            ]
    status                              = models.CharField(verbose_name='결제상태', default='await', choices=STATUS_CHOICES, max_length=10)


    @property
    def merchant_uid(self) -> str:
        return self.uid.hex