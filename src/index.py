from js import Response

async def on_fetch(request):
    return Response.new("我是跑在 Cloudflare Workers 上的 Python！")
