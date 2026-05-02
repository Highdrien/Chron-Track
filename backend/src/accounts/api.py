from ninja import Router
from ninja_jwt.authentication import JWTAuth
from ninja_jwt.tokens import RefreshToken

from accounts.models import User
from accounts.schemas import ErrorOut, RegisterIn, TokenPairOut, UserOut

router = Router(tags=["Auth"])


@router.post(
    "/register",
    response={201: TokenPairOut, 400: ErrorOut},
    auth=None,
    summary="Create a new account",
)
def register(request, payload: RegisterIn):
    if User.objects.filter(username=payload.username).exists():
        return 400, ErrorOut(detail="Username already in use.")

    if User.objects.filter(email=payload.email).exists():
        return 400, ErrorOut(detail="Email already in use.")

    user = User.objects.create_user(
        username=payload.username,
        password=payload.password,
        email=payload.email,
    )
    refresh = RefreshToken.for_user(user)
    return 201, TokenPairOut(access=str(refresh.access_token), refresh=str(refresh))


@router.get("/me", response=UserOut, auth=JWTAuth(), summary="Current user info")
def me(request):
    return request.user
