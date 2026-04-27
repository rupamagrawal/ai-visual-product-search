function ResultCard({ item }) {
  return (
    <article className="overflow-hidden rounded-2xl border border-slate-200 bg-white shadow-sm">
      {item.image ? (
        <img
          src={item.image}
          alt={item.title || "Product"}
          className="h-48 w-full object-cover"
        />
      ) : (
        <div className="flex h-48 items-center justify-center bg-slate-100 text-slate-500">
          No image
        </div>
      )}
      <div className="space-y-2 p-4">
        <h3 className="line-clamp-2 text-sm font-semibold text-slate-900">
          {item.title || "Untitled product"}
        </h3>
        <p className="text-sm text-slate-600">{item.price || "Price not listed"}</p>
        <p className="text-xs text-slate-500">{item.source || "Unknown source"}</p>
        {item.link ? (
          <a
            href={item.link}
            target="_blank"
            rel="noreferrer"
            className="inline-block text-sm font-medium text-blue-700 hover:underline"
          >
            View Product
          </a>
        ) : null}
      </div>
    </article>
  );
}

export default ResultCard;
