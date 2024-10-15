# signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import Users, Wholesaler, Buyer, Customer

@receiver(post_save, sender=Wholesaler)
def notify_wholesaler_approval(sender, instance, created, **kwargs):
    if not created:
        # 이전 상태와 현재 상태 비교
        previous_status = sender.objects.get(pk=instance.pk).approve_status
        if previous_status != instance.approve_status:
            # 승인 상태가 'approved'로 변경된 경우 알림을 보냅니다.
            if instance.approve_status == 'approved':
                # 이메일 알림 보내기 예시
                send_mail(
                    '도매업자 승인 알림',
                    f'{instance.company_name}님의 도매업자 신청이 승인되었습니다.',
                    'admin@example.com',  # 발신자 이메일
                    [instance.user.email],  # 수신자 이메일
                    fail_silently=False,
                )
                print(f'Wholesaler {instance.company_name} has been approved.')


@receiver(post_save, sender=Buyer)
def notify_buyer_approval(sender, instance, created, **kwargs):
    if not created:
        # 이전 상태와 현재 상태 비교
        previous_status = sender.objects.get(pk=instance.pk).approve_status
        if previous_status != instance.approve_status:
            # 승인 상태가 'approved'로 변경된 경우 알림을 보냅니다.
            if instance.approve_status == 'approved':
                # 이메일 알림 보내기 예시
                send_mail(
                    '구매자 승인 알림',
                    f'{instance.company_name}님의 구매자 신청이 승인되었습니다.',
                    'admin@example.com',  # 발신자 이메일
                    [instance.user.email],  # 수신자 이메일
                    fail_silently=False,
                )
                print(f'Buyer {instance.company_name} has been approved.')


