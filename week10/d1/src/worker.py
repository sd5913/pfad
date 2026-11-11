"""Week 4's request -> data -> JSON pattern, now backed by related D1 rows."""
from urllib.parse import parse_qs, urlparse
from workers import Response, WorkerEntrypoint

SQL = '''SELECT message.id, conversation.title, message.role, message.content
         FROM message JOIN conversation ON message.conversation_id = conversation.id
         WHERE conversation.id = ?1 ORDER BY message.id'''


class Default(WorkerEntrypoint):
    async def fetch(self, request):
        url = urlparse(request.url)
        if url.path != '/messages':
            return Response.json({'error': 'Use /messages?conversation=1'}, status=404)
        if request.method != 'GET':
            return Response.json({'error': 'This teaching API is read-only'}, status=405)
        try:
            values = parse_qs(url.query).get('conversation', [])
            if len(values) != 1 or not values[0].isascii() or not values[0].isdigit():
                raise ValueError()
            conversation = int(values[0])
            if not 1 <= conversation <= 2147483647:
                raise ValueError()
        except ValueError:
            return Response.json({'error': 'Use a positive integer conversation ID'}, status=400)
        result = await self.env.DB.prepare(SQL).bind(conversation).all()
        return Response.json(result)
