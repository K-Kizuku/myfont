# API定義書

##  method : GET , endpoint : "/" (動作確認用)
### レスポンス
```
{
    "message" : "welcome to myfont!"
}
```

## method : GET , endpoint : "/email/{address}" (addressはemailアドレス)
### レスポンス
なし。pathで指定したadressにメールが送信される。
