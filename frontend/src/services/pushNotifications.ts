const SUBSCRIPTION_KEY = "placementpro_push_subscription";

export function isPushSupported() {
  return "serviceWorker" in navigator && "PushManager" in window;
}

export function requestPushPermission() {
  if (typeof Notification === "undefined")
    return Promise.resolve("unsupported");
  return Notification.requestPermission();
}

export async function subscribeToPush() {
  if (!isPushSupported()) return null;
  try {
    const registration = await navigator.serviceWorker.ready;
    const subscription = await registration.pushManager.subscribe({
      userVisibleOnly: true,
    });
    const subscriptionJson = subscription.toJSON();
    localStorage.setItem(SUBSCRIPTION_KEY, JSON.stringify(subscriptionJson));
    return subscriptionJson;
  } catch (err) {
    return null;
  }
}

export function getStoredSubscription() {
  try {
    const raw = localStorage.getItem(SUBSCRIPTION_KEY);
    return raw ? JSON.parse(raw) : null;
  } catch (err) {
    return null;
  }
}
