
import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;

void main() {
  runApp(const CampusAIApp());
}

class CampusAIApp extends StatelessWidget {
  const CampusAIApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      title: 'CampusAI Assistant',
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(
          seedColor: const Color(0xFF123C69),
        ),
        useMaterial3: true,
      ),
      home: const ChatScreen(),
    );
  }
}

class ChatScreen extends StatefulWidget {
  const ChatScreen({super.key});

  @override
  State<ChatScreen> createState() => _ChatScreenState();
}

class _ChatScreenState extends State<ChatScreen> {
  final TextEditingController controller = TextEditingController();
  final ScrollController scrollController = ScrollController();

  final List<Map<String, dynamic>> messages = [];

  bool isLoading = false;

  static const String apiUrl =
      'http://127.0.0.1:5001/api/chat';

  Future<void> sendMessage() async {
    final question = controller.text.trim();

    if (question.isEmpty || isLoading) return;

    setState(() {
      messages.add({
        'type': 'user',
        'text': question,
      });
      controller.clear();
      isLoading = true;
    });

    scrollToBottom();

    try {
      final response = await http.post(
        Uri.parse(apiUrl),
        headers: {
          'Content-Type': 'application/json',
        },
        body: jsonEncode({
          'question': question,
        }),
      );

      final data = jsonDecode(response.body);

      if (response.statusCode != 200) {
        throw Exception(
          data['error'] ?? 'Unable to process your question.',
        );
      }

      setState(() {
        messages.add({
          'type': 'bot',
          'text': data['answer'] ?? 'No answer found.',
          'sources': data['sources'] ?? [],
          'disclaimer': data['disclaimer'] ?? '',
        });
      });
    } catch (error) {
      setState(() {
        messages.add({
          'type': 'bot',
          'text': 'Sorry, something went wrong.\n$error',
          'sources': [],
          'disclaimer': '',
        });
      });
    } finally {
      setState(() {
        isLoading = false;
      });
      scrollToBottom();
    }
  }

  void scrollToBottom() {
    WidgetsBinding.instance.addPostFrameCallback((_) {
      if (scrollController.hasClients) {
        scrollController.animateTo(
          scrollController.position.maxScrollExtent,
          duration: const Duration(milliseconds: 300),
          curve: Curves.easeOut,
        );
      }
    });
  }

  Widget buildMessage(Map<String, dynamic> message) {
    final isUser = message['type'] == 'user';

    return Align(
      alignment:
          isUser ? Alignment.centerRight : Alignment.centerLeft,
      child: Container(
        constraints: const BoxConstraints(maxWidth: 650),
        margin: const EdgeInsets.symmetric(vertical: 8),
        padding: const EdgeInsets.all(16),
        decoration: BoxDecoration(
          color: isUser
              ? const Color(0xFF123C69)
              : Colors.white,
          borderRadius: BorderRadius.circular(14),
          border: Border.all(
            color: isUser
                ? const Color(0xFF123C69)
                : Colors.grey.shade200,
          ),
        ),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            SelectableText(
              message['text'] ?? '',
              style: TextStyle(
                color: isUser ? Colors.white : Colors.black87,
                fontSize: 15,
                height: 1.5,
              ),
            ),

            if (!isUser &&
                (message['sources'] as List? ?? []).isNotEmpty) ...[
              const SizedBox(height: 14),
              const Text(
                'Sources',
                style: TextStyle(fontWeight: FontWeight.bold),
              ),
              const SizedBox(height: 8),

              ...(message['sources'] as List).map((source) {
                return Container(
                  margin: const EdgeInsets.only(bottom: 8),
                  padding: const EdgeInsets.all(10),
                  decoration: BoxDecoration(
                    color: const Color(0xFFF1F5F9),
                    borderRadius: BorderRadius.circular(8),
                  ),
                  child: Text(
                    '${source['document_title'] ?? 'Unknown document'}\n'
                    'Section: ${source['section_heading'] ?? 'Not specified'}\n'
                    'Version: ${source['version'] ?? 'Not specified'}\n'
                    'Page: ${source['page_number'] ?? 'Not specified'}',
                    style: const TextStyle(fontSize: 13),
                  ),
                );
              }),
            ],

            if (!isUser &&
                (message['disclaimer'] ?? '').isNotEmpty) ...[
              const SizedBox(height: 12),
              Text(
                message['disclaimer'],
                style: TextStyle(
                  fontSize: 11,
                  color: Colors.grey.shade700,
                ),
              ),
            ],
          ],
        ),
      ),
    );
  }

  @override
  void dispose() {
    controller.dispose();
    scrollController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFFF1F5F9),
      appBar: AppBar(
        backgroundColor: const Color(0xFF123C69),
        foregroundColor: Colors.white,
        title: const Row(
          children: [
            Icon(Icons.school, size: 30),
            SizedBox(width: 12),
            Text(
              'CampusAI Assistant',
              style: TextStyle(fontWeight: FontWeight.bold),
            ),
          ],
        ),
        actions: const [
          Padding(
            padding: EdgeInsets.only(right: 24),
            child: Center(
              child: Text('Maseno University'),
            ),
          ),
        ],
      ),

      body: Center(
        child: ConstrainedBox(
          constraints: const BoxConstraints(maxWidth: 950),
          child: Column(
            children: [
              const SizedBox(height: 24),

              const Text(
                'Welcome to CampusAI Assistant',
                style: TextStyle(
                  fontSize: 25,
                  fontWeight: FontWeight.bold,
                  color: Color(0xFF123C69),
                ),
                textAlign: TextAlign.center,
              ),

              const SizedBox(height: 8),

              const Text(
                'Your university information assistant',
                style: TextStyle(color: Colors.blueGrey),
              ),

              const Padding(
                padding: EdgeInsets.all(12),
                child: Text(
                  'Ask questions about university handbooks, policies and guidelines.',
                  textAlign: TextAlign.center,
                ),
              ),

              Expanded(
                child: Container(
                  margin: const EdgeInsets.symmetric(
                    horizontal: 16,
                    vertical: 10,
                  ),
                  padding: const EdgeInsets.all(16),
                  decoration: BoxDecoration(
                    color: const Color(0xFFF8FAFC),
                    borderRadius: BorderRadius.circular(14),
                    border: Border.all(color: Colors.grey.shade200),
                  ),
                  child: messages.isEmpty
                      ? const Center(
                          child: Column(
                            mainAxisAlignment: MainAxisAlignment.center,
                            children: [
                              Icon(
                                Icons.chat_bubble_outline,
                                size: 55,
                                color: Color(0xFF123C69),
                              ),
                              SizedBox(height: 15),
                              Text(
                                'Hello! How can I help you today?',
                                style: TextStyle(fontSize: 17),
                              ),
                            ],
                          ),
                        )
                      : ListView.builder(
                          controller: scrollController,
                          itemCount: messages.length,
                          itemBuilder: (context, index) {
                            return buildMessage(messages[index]);
                          },
                        ),
                ),
              ),

              if (isLoading)
                const Padding(
                  padding: EdgeInsets.all(8),
                  child: Row(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      SizedBox(
                        width: 18,
                        height: 18,
                        child: CircularProgressIndicator(strokeWidth: 2),
                      ),
                      SizedBox(width: 10),
                      Text('Searching university documents...'),
                    ],
                  ),
                ),

              Container(
                margin: const EdgeInsets.fromLTRB(16, 8, 16, 8),
                padding: const EdgeInsets.symmetric(horizontal: 12),
                decoration: BoxDecoration(
                  color: Colors.white,
                  borderRadius: BorderRadius.circular(12),
                  border: Border.all(color: Colors.grey.shade300),
                ),
                child: Row(
                  children: [
                    Expanded(
                      child: TextField(
                        controller: controller,
                        onSubmitted: (_) => sendMessage(),
                        decoration: const InputDecoration(
                          hintText: 'Type your university-related question...',
                          border: InputBorder.none,
                        ),
                      ),
                    ),
                    IconButton(
                      onPressed: isLoading ? null : sendMessage,
                      icon: const Icon(Icons.send),
                      color: const Color(0xFF123C69),
                      tooltip: 'Send',
                    ),
                  ],
                ),
              ),

              const Padding(
                padding: EdgeInsets.only(
                  bottom: 14,
                  left: 16,
                  right: 16,
                ),
                child: Text(
                  'CampusAI Assistant may make errors. Verify important information with the relevant university department.',
                  textAlign: TextAlign.center,
                  style: TextStyle(
                    fontSize: 11,
                    color: Colors.blueGrey,
                  ),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
