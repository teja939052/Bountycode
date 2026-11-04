import { useEffect, useState } from "react";
import { useParams, Link } from "react-router-dom";
import api from "../services/api";

export default function ArticlePage() {
  const { slug } = useParams<{ slug: string }>();
  const [blog, setBlog] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!slug) return;
    api.blog.get(slug).then((r: any) => {
      setBlog(r);
      setLoading(false);
    });
  }, [slug]);

  if (loading) return <p className="text-gray-500">Loading article…</p>;
  if (!blog) return <p className="text-red-600">Article not found.</p>;

  return (
    <div className="max-w-3xl mx-auto p-6 space-y-6">
      <nav className="mb-2">
        <Link to="/blogs" className="text-indigo-600 hover:underline">
          &larr; Back to blogs
        </Link>
      </nav>
      <div className="flex gap-2 mb-4">
        {blog.tags?.map((t: string) => (
          <span key={t} className="text-xs bg-indigo-50 px-2 py-1 rounded text-indigo-700 border border-indigo-100">
            {t}
          </span>
        ))}
      </div>
      <h1 className="text-3xl font-bold">{blog.title}</h1>
      <p className="text-gray-500 text-sm">
        By {blog.author} &middot; {blog.updated_at} &middot; {blog.topic}
      </p>
      <div className="prose prose-lg max-w-none">
        {blog.body
          .split("\n\n")
          .map((p: string, i: number) => (
            <p key={i} className="mb-4 leading-relaxed">
              {p}
            </p>
          ))}
      </div>
      {blog.code && (
        <div className="bg-gray-900 rounded-xl p-4 overflow-x-auto my-4 border border-gray-700">
          <pre className="text-sm text-green-300">{blog.code}</pre>
        </div>
      )}
      {blog.related_topic && (
        <div className="border-l-4 border-indigo-500 bg-indigo-50 p-4 rounded-r-xl my-6">
          <h3 className="font-bold text-indigo-800 mb-2">Practice it</h3>
          <p className="mb-2">Drill this concept with the <strong>{blog.topic}</strong> topic test:</p>
          <Link to={`/percentages-academy`} className="text-indigo-600 font-semibold hover:underline">
            Start the {blog.topic} practice &rarr;
          </Link>
        </div>
      )}
    </div>
  );
}
