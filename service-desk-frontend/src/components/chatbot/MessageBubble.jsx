const MessageBubble = ({ message }) => {
  const isUser = message.sender === "user";

  return (
    <div
      className={`d-flex ${isUser ? "justify-content-end" : "justify-content-start"}`}
    >
      <div
        className={`p-2 rounded mb-1 ${
          isUser ? "bg-primary text-white" : "bg-light"
        }`}
        style={{ maxWidth: "75%" }}
      >
        {message.text}
      </div>
    </div>
  );
};

export default MessageBubble;
