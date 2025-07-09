from fastapi import APIRouter

# separando as rotas da API

router = APIRouter(
    prefix='/api/v1/carros',
    tags=['carros'],
)


# Lista Teste
@router.get('/')
def lista_carros():
    return {
        'carros': [
            {'id': 1, 'modelo': 'Fusca'},
            {'id': 2, 'modelo': 'Opala'},
            {'id': 3, 'modelo': 'Chevet'},
        ]
    }
