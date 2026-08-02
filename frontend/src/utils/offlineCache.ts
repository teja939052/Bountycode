const DB_NAME = "placementpro";
const DB_VERSION = 1;
const STORE_NAME = "lessons";

let dbPromise = null;

function openDB() {
  if (dbPromise) return dbPromise;
  dbPromise = new Promise((resolve, reject) => {
    if (typeof indexedDB === "undefined") {
      reject(new Error("IndexedDB is not supported"));
      return;
    }
    const request = indexedDB.open(DB_NAME, DB_VERSION);
    request.onupgradeneeded = () => {
      const db = request.result;
      if (!db.objectStoreNames.contains(STORE_NAME)) {
        const store = db.createObjectStore(STORE_NAME, { keyPath: "key" });
        store.createIndex("languageId", "languageId", { unique: false });
      }
    };
    request.onsuccess = () => resolve(request.result);
    request.onerror = () => reject(request.error);
  });
  return dbPromise;
}

function withStore(mode, operation) {
  return openDB().then(
    (db) =>
      new Promise((resolve, reject) => {
        const tx = db.transaction(STORE_NAME, mode);
        const store = tx.objectStore(STORE_NAME);
        const request = operation(store);
        request.onsuccess = () => resolve(request.result);
        request.onerror = () => reject(request.error);
      })
  );
}

function lessonKey(languageId, lessonId) {
  return `${languageId}:${lessonId}`;
}

export async function saveLesson(languageId, lessonId, content) {
  const key = lessonKey(languageId, lessonId);
  await withStore("readwrite", (store) =>
    store.put({ key, languageId, lessonId, content, savedAt: Date.now() })
  );
  return key;
}

export async function getLesson(languageId, lessonId) {
  const record = await withStore("readonly", (store) =>
    store.get(lessonKey(languageId, lessonId))
  );
  return record ? record.content : null;
}

export async function getCachedLessonIds(languageId) {
  const keys = await withStore("readonly", (store) =>
    store.index("languageId").getAllKeys(languageId)
  );
  return keys.map((key) => String(key).split(":").slice(1).join(":"));
}

export async function getCachedLessonCount() {
  return withStore("readonly", (store) => store.count());
}
