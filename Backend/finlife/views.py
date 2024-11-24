import requests
from django.conf import settings
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import DepositProducts, DepositOptions, SavingProducts, SavingOptions
from .serializers import DepositProductsSerializer, DepositOptionsSerializer, SavingProductsSerializer, SavingOptionsSerializer


@api_view(['GET'])
def save_deposit_products(request):
    api_key = settings.API_KEY
    url = f"http://finlife.fss.or.kr/finlifeapi/depositProductsSearch.json?auth={api_key}&topFinGrpNo=020000&pageNo=1"
    response = requests.get(url).json()

    # Product 중복제거 및 저장
    for product in response.get('result', {}).get('baseList', []):
        fin_prdt_cd = product.get('fin_prdt_cd')
        if DepositProducts.objects.filter(fin_prdt_cd=fin_prdt_cd).exists():
            continue

        serializer = DepositProductsSerializer(data=product)
        if serializer.is_valid(raise_exception=True):
            serializer.save()

    # Options 중복제거 및 저장
    for option in response.get('result', {}).get('optionList', []):
        fin_prdt_cd = option.get('fin_prdt_cd')
        intr_rate_type_nm = option.get('intr_rate_type_nm')
        intr_rate = option.get('intr_rate')
        intr_rate2 = option.get('intr_rate2')
        save_trm = option.get('save_trm')

        deposit_product = DepositProducts.objects.filter(fin_prdt_cd=fin_prdt_cd).first()
        if DepositOptions.objects.filter(
            product=deposit_product.id,
            intr_rate_type_nm=intr_rate_type_nm,
            intr_rate=intr_rate,
            intr_rate2=intr_rate2,
        ).exists():
            continue

        option_data = {
            'fin_prdt_cd': deposit_product.fin_prdt_cd,
            'intr_rate_type_nm': intr_rate_type_nm,
            'intr_rate': intr_rate if intr_rate is not None else -1,
            'intr_rate2': intr_rate2 if intr_rate2 is not None else -1,
            'save_trm': save_trm,
        }
        serializer = DepositOptionsSerializer(data=option_data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(product=deposit_product)

    return JsonResponse({'message': '저장 성공'})


@api_view(['GET', 'POST'])
def deposit_products(request):
    if request.method == 'GET':
        products = DepositProducts.objects.all()
        serializer = DepositProductsSerializer(products, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = DepositProductsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse({'message': '데이터 저장 실패 또는 중복'})


@api_view(['GET'])
def deposit_product_options(request, fin_prdt_cd):
    product = DepositProducts.objects.get(fin_prdt_cd=fin_prdt_cd)
    options = DepositOptions.objects.filter(product=product.id)
    serializer = DepositOptionsSerializer(options, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def top_rate(request):
    top_option = DepositOptions.objects.order_by('-intr_rate2').first()
    if top_option:
        product = top_option.product
        product_serializer = DepositProductsSerializer(product)
        option_serializer = DepositOptionsSerializer(top_option)
        return Response({
            'product': product_serializer.data,
            'option': option_serializer.data,
        })
    return Response({"message": "데이터 없음"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def save_saving_products(request):
    api_key = settings.API_KEY
    url = f"http://finlife.fss.or.kr/finlifeapi/savingProductsSearch.json?auth={api_key}&topFinGrpNo=020000&pageNo=1"
    response = requests.get(url).json()

    # Product 중복제거 및 저장
    for product in response.get('result', {}).get('baseList', []):
        fin_prdt_cd = product.get('fin_prdt_cd')
        if SavingProducts.objects.filter(fin_prdt_cd=fin_prdt_cd).exists():
            continue

        serializer = SavingProductsSerializer(data=product)
        if serializer.is_valid(raise_exception=True):
            serializer.save()

    # Options 중복제거 및 저장
    for option in response.get('result', {}).get('optionList', []):
        fin_prdt_cd = option.get('fin_prdt_cd')
        intr_rate_type_nm = option.get('intr_rate_type_nm')
        rsrv_type_nm = option.get('rsrv_type_nm')
        intr_rate = option.get('intr_rate')
        intr_rate2 = option.get('intr_rate2')
        save_trm = option.get('save_trm')

        saving_product = SavingProducts.objects.filter(fin_prdt_cd=fin_prdt_cd).first()
        if SavingOptions.objects.filter(
            product=saving_product.id,
            intr_rate_type_nm=intr_rate_type_nm,
            intr_rate=intr_rate,
            intr_rate2=intr_rate2,
        ).exists():
            continue

        option_data = {
            'fin_prdt_cd': saving_product.fin_prdt_cd,
            'intr_rate_type_nm': intr_rate_type_nm,
            'rsrv_type_nm': rsrv_type_nm,
            'intr_rate': intr_rate if intr_rate is not None else -1,
            'intr_rate2': intr_rate2 if intr_rate2 is not None else -1,
            'save_trm': save_trm,
        }
        serializer = SavingOptionsSerializer(data=option_data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(product=saving_product)

    return JsonResponse({'message': '저장 성공'})


@api_view(['GET', 'POST'])
def saving_products(request):
    if request.method == 'GET':
        products = SavingProducts.objects.all()
        serializer = SavingProductsSerializer(products, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = SavingProductsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse({'message': '데이터 저장 실패 또는 중복'})


@api_view(['GET'])
def saving_product_options(request, fin_prdt_cd):
    product = SavingProducts.objects.get(fin_prdt_cd=fin_prdt_cd)
    options = SavingOptions.objects.filter(product=product.id)
    serializer = SavingOptionsSerializer(options, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def top_saving_rate(request):
    top_option = SavingOptions.objects.order_by('-intr_rate2').first()
    if top_option:
        product = top_option.product
        product_serializer = SavingProductsSerializer(product)
        option_serializer = SavingOptionsSerializer(top_option)
        return Response({
            'product': product_serializer.data,
            'option': option_serializer.data,
        })
    return Response({"message": "데이터 없음"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def product_list(request):
    """
    전체 상품 목록 반환 (예금 + 적금)
    """
    bank_name = request.query_params.get('bank', None)
    deposit_products = DepositProducts.objects.all()
    saving_products = SavingProducts.objects.all()

    if bank_name:
        deposit_products = deposit_products.filter(kor_co_nm__icontains=bank_name)
        saving_products = saving_products.filter(kor_co_nm__icontains=bank_name)

    deposit_list = []
    for product in deposit_products:
        options = DepositOptions.objects.filter(product=product)
        interest_rates = {opt.save_trm: opt.intr_rate for opt in options}
        deposit_list.append({
            "id": product.id,
            "type": "deposit",
            "kor_co_nm": product.kor_co_nm,
            "fin_prdt_nm": product.fin_prdt_nm,
            "interest_rates": {
                "6": interest_rates.get(6, "-"),
                "12": interest_rates.get(12, "-"),
                "24": interest_rates.get(24, "-"),
                "36": interest_rates.get(36, "-"),
            }
        })

    saving_list = []
    for product in saving_products:
        options = SavingOptions.objects.filter(product=product)
        interest_rates = {opt.save_trm: opt.intr_rate for opt in options}
        saving_list.append({
            "id": product.id,
            "type": "saving",
            "kor_co_nm": product.kor_co_nm,
            "fin_prdt_nm": product.fin_prdt_nm,
            "interest_rates": {
                "6": interest_rates.get(6, "-"),
                "12": interest_rates.get(12, "-"),
                "24": interest_rates.get(24, "-"),
                "36": interest_rates.get(36, "-"),
            }
        })

    return Response({
        "deposits": deposit_list,
        "savings": saving_list
    })



@api_view(['GET'])
def product_detail(request, product_type, product_id):
    """
    특정 상품 상세 정보 반환
    product_type: 'deposit' 또는 'saving'
    product_id: 상품 ID
    """
    if product_type == 'deposit':
        product = DepositProducts.objects.filter(id=product_id).first()
        if not product:
            return Response({"error": "Deposit product not found"}, status=404)
        options = DepositOptions.objects.filter(product=product).order_by('save_trm')
        product_serializer = DepositProductsSerializer(product)
        option_serializer = DepositOptionsSerializer(options, many=True)
        return Response({
            "product": product_serializer.data,
            "options": option_serializer.data
        })

    elif product_type == 'saving':
        product = SavingProducts.objects.filter(id=product_id).first()
        if not product:
            return Response({"error": "Saving product not found"}, status=404)
        options = SavingOptions.objects.filter(product=product).order_by('save_trm')
        product_serializer = SavingProductsSerializer(product)
        option_serializer = SavingOptionsSerializer(options, many=True)
        return Response({
            "product": product_serializer.data,
            "options": option_serializer.data
        })

    return Response({"error": "Invalid product type"}, status=400)



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def join_product(request):
    """
    금융상품 가입
    """
    print('받은 데이터:', request.data)  # 디버깅용 로그
    product_type = request.data.get('product_type')
    product_id = request.data.get('product_id')
    
    if not product_type or not product_id:
        return Response(
            {'message': '상품 타입과 ID가 필요합니다.'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    user = request.user
    current_products = user.fin_products.split(',') if user.fin_products else []
    new_product = f"{product_type}:{product_id}"
    
    if new_product not in current_products:
        current_products.append(new_product)
        user.fin_products = ','.join(filter(None, current_products))
        user.save()
        
    return Response({
        "message": "상품 가입이 완료되었습니다.",
        "fin_products": user.fin_products
    })

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def cancel_product(request):
    """
    금융상품 해지
    """
    product_type = request.data.get('product_type')
    product_id = request.data.get('product_id')
    
    if not product_type or not product_id:
        return Response({"error": "상품 정보가 필요합니다."}, status=400)
    
    user = request.user
    current_products = user.fin_products.split(',') if user.fin_products else []
    product_to_remove = f"{product_type}:{product_id}"
    
    if product_to_remove in current_products:
        current_products.remove(product_to_remove)
        user.fin_products = ','.join(filter(None, current_products))
        user.save()
        
    return Response({
        "message": "상품이 해지되었습니다.",
        "fin_products": user.fin_products
    })

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_products(request):
    """
    사용자의 가입 상품 목록 조회
    """
    user = request.user
    if not user.fin_products:
        return Response({"products": []})
    
    product_list = [p for p in user.fin_products.split(',') if p]
    products = []
    
    for product_info in product_list:
        try:
            product_type, product_id = product_info.split(':')
            if product_type == 'deposit':
                product = get_object_or_404(DepositProducts, id=product_id)
                serializer = DepositProductsSerializer(product)
            elif product_type == 'saving':
                product = get_object_or_404(SavingProducts, id=product_id)
                serializer = SavingProductsSerializer(product)
            else:
                continue
            products.append({
                'type': product_type,
                'product': serializer.data
            })
        except Exception as e:
            print(f"Error processing product {product_info}: {str(e)}")
            continue
            
    return Response({"products": products})