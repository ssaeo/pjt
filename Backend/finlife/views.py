import requests
from django.conf import settings
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.http import JsonResponse
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
        options = DepositOptions.objects.filter(product=product)
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
        options = SavingOptions.objects.filter(product=product)
        product_serializer = SavingProductsSerializer(product)
        option_serializer = SavingOptionsSerializer(options, many=True)
        return Response({
            "product": product_serializer.data,
            "options": option_serializer.data
        })

    return Response({"error": "Invalid product type"}, status=400)