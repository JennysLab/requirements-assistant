import PageHeader from "../components/common/PageHeader.jsx";
import PlaceholderNotice from "../components/common/PlaceholderNotice.jsx";
import ChatWindow from "../components/chat/ChatWindow.jsx";
import DocumentList from "../components/knowledgebase/DocumentList.jsx";

export default function BuddyPage() {
  return (
    <>
      <PageHeader title="Virtual Buddy" subtitle="Fragen zum System und zur Wissensbasis." />
      <div className="mb-4"><PlaceholderNotice>Der Buddy antwortet nur aus den hochgeladenen Dokumenten und nennt die Quellen. Dokumente lädst du links hoch.</PlaceholderNotice></div>
      <div className="grid gap-6 md:grid-cols-[320px_1fr]">
        <DocumentList />
        <div className="h-[520px]"><ChatWindow /></div>
      </div>
    </>
  );
}
