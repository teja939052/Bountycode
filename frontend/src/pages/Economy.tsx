import { useState, useEffect } from "react";
import api from "../services/api";
import { useJuice } from "../juice/JuiceProvider";

export default function Economy() {
  const { showXP, play } = useJuice();
  const [balance, setBalance] = useState(0);
  const [inventory, setInventory] = useState([]);
  const [shopItems, setShopItems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [message, setMessage] = useState("");
  const [activeTab, setActiveTab] = useState("shop");

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      const [balanceData, shopData] = await Promise.all([
        api.economy?.getBalance?.() || { balance: 0, inventory: [] },
        api.economy?.getShop?.() || { items: {} },
      ]);
      setBalance(balanceData.balance || 0);
      setInventory(balanceData.inventory || []);
      setShopItems(Object.entries(shopData.items || {}));
    } catch {
      setBalance(0);
      setInventory([]);
      setShopItems([]);
    } finally {
      setLoading(false);
    }
  };

  const handleDailyBonus = async () => {
    setLoading(true);
    try {
      const data = await api.economy?.dailyBonus?.() || {};
      setMessage(`+${data.earned || 10} ${data.currency || "🪙"}!`);
      play("xpCollect");
      showXP(data.earned || 10, window.innerWidth / 2, window.innerHeight / 2);
      await loadData();
    } catch (err) {
      setMessage(err.message || "Already claimed today");
    } finally {
      setLoading(false);
    }
  };

  const handleBuyItem = async (itemId) => {
    setLoading(true);
    try {
      const data = await api.economy?.buy?.({ item_id: itemId }) || {};
      setMessage(`Purchased ${data.item} for ${data.cost} 🪙!`);
      play("badgeUnlock");
      showXP(data.cost || 10, window.innerWidth / 2, window.innerHeight / 2);
      await loadData();
    } catch (err) {
      setMessage(err.message || "Purchase failed");
    } finally {
      setLoading(false);
    }
  };

  const handleSellItem = async (itemId) => {
    setLoading(true);
    try {
      const data = await api.economy?.sell?.({ item_id: itemId }) || {};
      setMessage(`Sold for ${data.earned || 1} 🪙!`);
      play("xpCollect");
      showXP(data.earned || 1, window.innerWidth / 2, window.innerHeight / 2);
      await loadData();
    } catch (err) {
      setMessage(err.message || "Sale failed");
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-gray-400 text-lg">Loading economy...</div>
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto p-6 space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-3xl font-bold text-gray-900">💰 Economy</h1>
        <div className="flex items-center gap-2">
          <span className="text-2xl">🪙</span>
          <span className="text-2xl font-bold text-indigo-600">{balance}</span>
          <span className="text-sm text-gray-500">PlacementCoin</span>
        </div>
      </div>

      {message && (
        <div className="bg-green-50 border border-green-200 text-green-700 px-4 py-3 rounded-lg text-sm">
          {message}
        </div>
      )}

      <div className="flex gap-3">
        <button
          onClick={handleDailyBonus}
          disabled={loading}
          className="px-4 py-2 bg-amber-500 text-white rounded-lg text-sm font-medium hover:bg-amber-600 disabled:opacity-50"
        >
          🎁 Daily Bonus (+10 🪙)
        </button>
        <button
          onClick={() => setActiveTab("inventory")}
          className={`px-4 py-2 rounded-lg text-sm font-medium ${activeTab === "inventory" ? "bg-indigo-600 text-white" : "bg-surface-card/50 text-brand-primary"}`}
        >
          Inventory ({inventory.length})
        </button>
        <button
          onClick={() => setActiveTab("shop")}
          className={`px-4 py-2 rounded-lg text-sm font-medium ${activeTab === "shop" ? "bg-indigo-600 text-white" : "bg-surface-card/50 text-brand-primary"}`}
        >
          Shop
        </button>
      </div>

      {activeTab === "shop" && (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {shopItems.map(([itemId, item]) => (
            <div
              key={itemId}
              className={`bg-surface-card border rounded-xl p-4 ${inventory.includes(itemId) ? "border-green-300" : "border-brand-primary/10"}`}
            >
              <div className="flex items-center gap-3 mb-2">
                <span className="text-2xl">{item.emoji}</span>
                <div>
                  <h3 className="font-semibold text-sm">{item.name}</h3>
                  <span className="text-xs px-2 py-0.5 rounded-full bg-surface-card/50 text-brand-secondary capitalize">
                    {item.rarity}
                  </span>
                </div>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-sm font-semibold text-amber-600">{item.cost} 🪙</span>
                {inventory.includes(itemId) ? (
                  <button
                    onClick={() => handleSellItem(itemId)}
                    disabled={loading}
                    className="px-3 py-1 bg-red-50 text-red-600 rounded-lg text-xs font-medium hover:bg-red-100"
                  >
                    Sell
                  </button>
                ) : (
                  <button
                    onClick={() => handleBuyItem(itemId)}
                    disabled={loading}
                    className="px-3 py-1 bg-indigo-600 text-white rounded-lg text-xs font-medium hover:bg-indigo-700 disabled:opacity-50"
                  >
                    Buy
                  </button>
                )}
              </div>
            </div>
          ))}
        </div>
      )}

      {activeTab === "inventory" && (
        <div className="bg-surface-card border border-brand-primary/10 rounded-xl p-6">
          {inventory.length === 0 ? (
            <div className="text-center py-8 text-gray-400">
              <div className="text-4xl mb-4">🎒</div>
              <p>Your inventory is empty. Visit the shop to buy items!</p>
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {inventory.map((itemId) => {
                const item = shopItems.find(([id]) => id === itemId)?.[1];
                if (!item) return null;
                return (
                  <div key={itemId} className="bg-surface-base border border-brand-primary/10 rounded-xl p-4">
                    <div className="flex items-center gap-3">
                      <span className="text-2xl">{item.emoji}</span>
                      <div>
                        <h3 className="font-semibold text-sm">{item.name}</h3>
                        <span className="text-xs text-gray-500 capitalize">{item.rarity}</span>
                      </div>
                    </div>
                    <button
                      onClick={() => handleSellItem(itemId)}
                      disabled={loading}
                      className="mt-3 w-full px-3 py-1.5 bg-red-50 text-red-600 rounded-lg text-xs font-medium hover:bg-red-100"
                    >
                      Sell for {Math.max(1, Math.floor(item.cost * 0.5))} 🪙
                    </button>
                  </div>
                );
              })}
            </div>
          )}
        </div>
      )}
    </div>
  );
}