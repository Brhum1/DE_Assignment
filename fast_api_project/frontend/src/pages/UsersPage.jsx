import { useEffect, useState, useCallback } from 'react';
import api from '../api/client';
import TaskList from '../components/TaskList';

const UsersPage = () => {
  const [users, setUsers] = useState([]);
  const [allProjects, setAllProjects] = useState([]); // تخزين كل المشاريع للفلترة
  const [formData, setFormData] = useState({ username: '', email: '', password: '' });
  const [editingId, setEditingId] = useState(null);
  const [expandedUserId, setExpandedUserId] = useState(null); // ID المستخدم المختار حالياً
  const [isLoadingProjects, setIsLoadingProjects] = useState(false);

  // 1. جلب المستخدمين
  const fetchUsers = useCallback(async () => {
    try {
      const res = await api.get('/users/');
      setUsers(res.data);
    } catch (err) {
      console.error("خطأ في جلب المستخدمين", err);
    }
  }, []);

  // 2. جلب كل المشاريع لفلترتها حسب المستخدم
  const fetchAllProjects = useCallback(async () => {
    setIsLoadingProjects(true);
    try {
      const res = await api.get('/projects/');
      setAllProjects(res.data);
    } catch (err) {
      console.error("خطأ في جلب المشاريع", err);
    } finally {
      setIsLoadingProjects(false);
    }
  }, []);

  useEffect(() => {
    let isMounted = true;
    const loadData = async () => {
      if (isMounted) await fetchUsers();
    };
    loadData();
    return () => { isMounted = false; };
  }, [fetchUsers]);

  // دالة التعامل مع فتح/إغلاق قسم المهام
  const toggleUserTasks = (userId) => {
    if (expandedUserId === userId) {
      setExpandedUserId(null);
    } else {
      setExpandedUserId(userId);
      fetchAllProjects(); // جلب المشاريع عند فتح القسم
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      if (editingId) {
        await api.put(`/users/${editingId}`, formData);
        setEditingId(null);
      } else {
        await api.post('/users/', formData);
      }
      setFormData({ username: '', email: '', password: '' });
      fetchUsers();
    } catch (err) {
      console.error("حدث خطأ أثناء حفظ البيانات:", err);
      alert("حدث خطأ في العملية، تأكد من البيانات");
    }
  };

  const handleEdit = (user) => {
    setEditingId(user.id);
    setFormData({ username: user.username, email: user.email, password: '' });
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  const deleteUser = async (id) => {
    if (window.confirm('حذف المستخدم سيؤدي لحذف كافة مشاريعه ومهامه، هل أنت متأكد؟')) {
      try {
        await api.delete(`/users/${id}`);
        setUsers((prev) => prev.filter(u => u.id !== id));
        if (expandedUserId === id) setExpandedUserId(null);
      } catch (err) {
        console.error("فشل الحذف", err);
      }
    }
  };

  return (
    <div className="space-y-6" dir="rtl">
      {/* نموذج الإضافة والتعديل */}
      <div className="bg-white p-6 rounded-3xl shadow-sm border border-gray-100">
        <h3 className="text-xl font-bold text-gray-800 mb-4 flex items-center gap-2">
          {editingId ? '📝 تعديل بيانات المستخدم' : '👤 إضافة مستخدم جديد'}
        </h3>
        <form onSubmit={handleSubmit} className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <input 
            className="p-3 bg-gray-50 border border-gray-200 rounded-xl outline-none focus:ring-2 focus:ring-indigo-500"
            placeholder="اسم المستخدم" 
            value={formData.username} 
            onChange={(e) => setFormData({...formData, username: e.target.value})}
            required 
          />
          <input 
            className="p-3 bg-gray-50 border border-gray-200 rounded-xl outline-none focus:ring-2 focus:ring-indigo-500"
            type="email" 
            placeholder="البريد الإلكتروني" 
            value={formData.email} 
            onChange={(e) => setFormData({...formData, email: e.target.value})}
            required 
          />
          <input 
            className="p-3 bg-gray-50 border border-gray-200 rounded-xl outline-none focus:ring-2 focus:ring-indigo-500"
            type="password" 
            placeholder={editingId ? "كلمة مرور جديدة (اختياري)" : "كلمة المرور"} 
            value={formData.password} 
            onChange={(e) => setFormData({...formData, password: e.target.value})}
            required={!editingId} 
          />
          <button className={`p-3 rounded-xl text-white font-bold transition-all cursor-pointer shadow-lg ${editingId ? 'bg-orange-500 hover:bg-orange-600' : 'bg-indigo-600 hover:bg-indigo-700'}`}>
            {editingId ? 'تحديث البيانات' : 'إضافة مستخدم'}
          </button>
        </form>
      </div>

      {/* جدول المستخدمين */}
      <div className="bg-white rounded-3xl shadow-sm border border-gray-100 overflow-hidden">
        <table className="w-full text-right border-collapse">
          <thead>
            <tr className="bg-gray-50 text-gray-600 text-sm">
              <th className="py-4 px-6">المستخدم</th>
              <th className="py-4 px-6">البريد الإلكتروني</th>
              <th className="py-4 px-6 text-center">الإجراءات</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-100">
            {users.map(user => (
              <tr key={user.id} className="hover:bg-gray-50/50 transition-colors">
                <td className="py-4 px-6">
                  <div className="font-bold text-gray-800">{user.username}</div>
                  <div className="text-[10px] text-gray-400 font-mono">ID: #{user.id}</div>
                </td>
                <td className="py-4 px-6 text-gray-600">{user.email}</td>
                <td className="py-4 px-6">
                  <div className="flex justify-center gap-2 font-bold text-xs">
                    <button onClick={() => handleEdit(user)} className="text-blue-600 bg-blue-50 px-3 py-2 rounded-lg hover:bg-blue-100 cursor-pointer">تعديل</button>
                    <button 
                       onClick={() => toggleUserTasks(user.id)} 
                       className={`px-3 py-2 rounded-lg cursor-pointer transition-all ${expandedUserId === user.id ? 'bg-indigo-600 text-white' : 'bg-indigo-50 text-indigo-600 hover:bg-indigo-100'}`}
                    >
                      {expandedUserId === user.id ? 'إغلاق المهام ↑' : 'عرض المهام ↓'}
                    </button>
                    <button onClick={() => deleteUser(user.id)} className="text-red-600 bg-red-50 px-3 py-2 rounded-lg hover:bg-red-100 cursor-pointer">حذف</button>
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* قسم إدارة المهام للمستخدم المختار */}
      {expandedUserId && (
        <div className="bg-indigo-50 p-6 rounded-3xl border border-indigo-100 animate-in fade-in slide-in-from-top-4">
          <div className="flex justify-between items-center mb-6">
            <h4 className="text-indigo-800 font-bold text-lg flex items-center gap-2">
              🚀 مشاريع ومهام المستخدم #{expandedUserId}
            </h4>
            {isLoadingProjects && <span className="text-xs text-indigo-400 animate-pulse">جاري جلب البيانات...</span>}
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {allProjects.filter(p => p.owner_id === expandedUserId).length > 0 ? (
              allProjects.filter(p => p.owner_id === expandedUserId).map(project => (
                <div key={project.id} className="bg-white p-5 rounded-2xl shadow-sm border border-indigo-50 flex flex-col">
                  <div className="mb-4">
                    <h5 className="font-bold text-gray-900">{project.title}</h5>
                    <p className="text-xs text-gray-500">{project.description || "لا يوجد وصف للمشروع"}</p>
                  </div>
                  
                  {/* استدعاء TaskList لإدارة مهام هذا المشروع */}
                  <TaskList projectId={project.id} />
                  
                  <div className="mt-4 pt-4 border-t border-gray-50 text-[9px] text-gray-400">
                    رقم المشروع: #{project.id}
                  </div>
                </div>
              ))
            ) : !isLoadingProjects && (
              <div className="col-span-full py-10 text-center bg-white/50 rounded-2xl border-2 border-dashed border-indigo-200 text-indigo-400 text-sm">
                لا توجد مشاريع مسجلة لهذا المستخدم حتى الآن.
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
};

export default UsersPage;