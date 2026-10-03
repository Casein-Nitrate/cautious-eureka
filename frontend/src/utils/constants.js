export const LANGUAGES = {
  en: { code: 'en', name: 'English', speechCode: 'en-IN' },
  hi: { code: 'hi', name: 'हिन्दी', speechCode: 'hi-IN' },
  mr: { code: 'mr', name: 'मराठी', speechCode: 'mr-IN' },
};
export const SPEAKERS = {
  learner: { label: 'Learner', color: '#2563eb' },
  parent: { label: 'Parent', color: '#059669' },
  guardian: { label: 'Guardian', color: '#7c3aed' },
};
export const TRADES = [
  'Solar Technician',
  'Electrician',
  'Plumber',
  'Welder',
  'CNC Operator',
  'Beauty & Wellness',
  'Healthcare Assistant',
  'Draughtsman Civil',
  'Refrigeration & AC Technician',
  'Food Processing Technician',
];
export const EDUCATION_LEVELS = ['Below Class 10', 'Class 10', 'Class 12', 'ITI', 'Diploma', 'Graduate'];
export const INCOME_BRACKETS = [
  { value: '<10k', label: 'Below ₹10,000' },
  { value: '10k-20k', label: '₹10,000 – ₹20,000' },
  { value: '20k-50k', label: '₹20,000 – ₹50,000' },
  { value: '>50k', label: 'Above ₹50,000' },
];
export const DISTRICTS = [
  ['Nashik', 'Maharashtra'], ['Pune', 'Maharashtra'], ['Mumbai', 'Maharashtra'], ['Aurangabad', 'Maharashtra'],
  ['Nagpur', 'Maharashtra'], ['Kolhapur', 'Maharashtra'], ['Solapur', 'Maharashtra'], ['Thane', 'Maharashtra'],
  ['Lucknow', 'Uttar Pradesh'], ['Varanasi', 'Uttar Pradesh'], ['Kanpur', 'Uttar Pradesh'],
  ['Patna', 'Bihar'], ['Gaya', 'Bihar'], ['Jaipur', 'Rajasthan'], ['Jodhpur', 'Rajasthan'],
  ['Ahmedabad', 'Gujarat'], ['Surat', 'Gujarat'], ['Bengaluru', 'Karnataka'], ['Mysuru', 'Karnataka'],
  ['Chennai', 'Tamil Nadu'], ['Coimbatore', 'Tamil Nadu'], ['Hyderabad', 'Telangana'],
  ['Bhopal', 'Madhya Pradesh'], ['Indore', 'Madhya Pradesh'], ['Raipur', 'Chhattisgarh'], ['Ranchi', 'Jharkhand'],
  ['Kolkata', 'West Bengal'], ['Khordha', 'Odisha'], ['Ganjam', 'Odisha'], ['Rayagada', 'Odisha'],
].map(([district, state]) => ({ district, state }));
export const CONCERN_LABELS = {
  income: 'Income', employment: 'Employment', safety: 'Safety', social_perception: 'Social perception',
  education_progression: 'Education progression', gender_family: 'Gender & family', information_gap: 'Information gap',
};
export const STATUS = {
  open: { label: 'Open', color: '#ef4444', icon: '🔴' },
  partially_resolved: { label: 'Partially resolved', color: '#f59e0b', icon: '🟡' },
  resolved: { label: 'Resolved', color: '#10b981', icon: '🟢' },
  not_raised: { label: 'Not raised', color: '#94a3b8', icon: '⚪' },
};
export const CASE_STATUS = { pending: 'Pending', in_progress: 'In progress', resolved: 'Resolved' };

export const T = {
  en: {
    title: 'Understand the career before you decide',
    sub: 'Talk through your worries about vocational training with an assistant that answers from verified job and earnings data.',
    start: 'Start counselling', send: 'Send',
    ph_learner: 'Ask your question as the learner…', ph_parent: 'Ask your question as the parent…', ph_guardian: 'Ask your question as the guardian…',
    escTitle: 'A human counsellor will help', escBody: 'Your concern needs personal guidance. A counsellor will review your case and contact you soon.',
  },
  hi: {
    title: 'फ़ैसले से पहले करियर को समझें',
    sub: 'व्यावसायिक प्रशिक्षण को लेकर अपनी चिंताएँ ऐसे सहायक से साझा करें जो सत्यापित रोज़गार और कमाई के आँकड़ों से जवाब देता है।',
    start: 'परामर्श शुरू करें', send: 'भेजें',
    ph_learner: 'शिक्षार्थी के रूप में अपना सवाल लिखें…', ph_parent: 'अभिभावक के रूप में अपना सवाल लिखें…', ph_guardian: 'संरक्षक के रूप में अपना सवाल लिखें…',
    escTitle: 'एक मानव परामर्शदाता आपकी मदद करेंगे', escBody: 'आपकी चिंता के लिए व्यक्तिगत मार्गदर्शन चाहिए। परामर्शदाता आपके केस की समीक्षा कर जल्द संपर्क करेंगे।',
  },
  mr: {
    title: 'निर्णयापूर्वी करिअर समजून घ्या',
    sub: 'व्यावसायिक प्रशिक्षणाबद्दलच्या तुमच्या शंका, पडताळलेल्या नोकरी व कमाईच्या आकडेवारीवर उत्तर देणाऱ्या सहाय्यकाशी बोला.',
    start: 'समुपदेशन सुरू करा', send: 'पाठवा',
    ph_learner: 'विद्यार्थी म्हणून तुमचा प्रश्न लिहा…', ph_parent: 'पालक म्हणून तुमचा प्रश्न लिहा…', ph_guardian: 'संरक्षक म्हणून तुमचा प्रश्न लिहा…',
    escTitle: 'मानवी समुपदेशक तुम्हाला मदत करतील', escBody: 'तुमच्या शंकेसाठी वैयक्तिक मार्गदर्शन आवश्यक आहे. समुपदेशक तुमच्या केसचा आढावा घेऊन लवकरच संपर्क करतील.',
  },
};
export const getLang = () => localStorage.getItem('lang') || 'en';
export const humanize = (s = '') => s.replace(/_/g, ' ').replace(/^./, (c) => c.toUpperCase());
