export interface Situation {
	emoji: string;
	title: string;
	body: string;
	cta: string;
	msg: string;
}

export interface Solution {
	title: string;
	body: string;
}

export interface Reason {
	emoji: string;
	title: string;
	body: string;
}

export interface Step {
	n: string;
	title: string;
	body: string;
}

export interface Review {
	name: string;
	area: string;
	text: string;
}

export interface Faq {
	q: string;
	a: string;
}

export const situations: Situation[] = [
	{ emoji: '🧱', title: 'Baru Renovasi', body: 'Dibuangi debu, sisa semen, dan bekas cat hingga siap ditempati.', cta: 'Saya baru renovasi', msg: 'Halo Tentram, saya baru selesai renovasi rumah dan butuh pembersihan. Boleh minta penawaran?' },
	{ emoji: '📦', title: 'Baru Pindahan', body: 'Setiap sudut dibersihkan sebelum Anda mulai menempati.', cta: 'Saya baru pindahan', msg: 'Halo Tentram, saya baru pindah rumah dan ingin move in cleaning. Boleh minta penawaran?' },
	{ emoji: '🏠', title: 'Rumah Terasa Kotor', body: 'Tidak sempat membersihkan sendiri? Biarkan kami membantu.', cta: 'Saya butuh home cleaning', msg: 'Halo Tentram, saya butuh home cleaning untuk rumah saya. Boleh minta penawaran?' },
	{ emoji: '🏢', title: 'Office Cleaning', body: 'Lingkungan kerja yang lebih nyaman untuk tim dan pelanggan.', cta: 'Saya butuh office cleaning', msg: 'Halo Tentram, kantor kami butuh cleaning rutin/berkala. Boleh minta penawaran?' },
	{ emoji: '✨', title: 'Deep Cleaning', body: 'Pembersihan menyeluruh hingga area yang jarang dibersihkan.', cta: 'Lihat deep cleaning', msg: 'Halo Tentram, saya tertarik dengan layanan Deep Cleaning. Boleh minta penawaran?' },
];

export const solutions: Solution[] = [
	{ title: 'Home Cleaning', body: 'Rumah bersih untuk aktivitas sehari-hari.' },
	{ title: 'Deep Cleaning', body: 'Pembersihan detail hingga sudut ruangan.' },
	{ title: 'Post Renovation', body: 'Membersihkan rumah setelah renovasi selesai.' },
	{ title: 'Move In Cleaning', body: 'Masuk rumah baru dengan lebih nyaman.' },
	{ title: 'Office Cleaning', body: 'Layanan cleaning rutin maupun berkala.' },
];

export const reasons: Reason[] = [
	{ emoji: '👥', title: 'Tim Profesional', body: 'Tim yang telah mendapatkan pelatihan.' },
	{ emoji: '⏰', title: 'Tepat Waktu', body: 'Datang sesuai jadwal.' },
	{ emoji: '🏷️', title: 'Harga Transparan', body: 'Tidak ada biaya tersembunyi.' },
	{ emoji: '🧰', title: 'Peralatan Lengkap', body: 'Tidak perlu menyiapkan alat sendiri.' },
	{ emoji: '💬', title: 'Fast Response', body: 'Booking mudah melalui WhatsApp.' },
	{ emoji: '✅', title: 'Quality Checklist', body: 'Setiap pekerjaan mengikuti standar operasional.' },
];

export const steps: Step[] = [
	{ n: '1', title: 'Hubungi WhatsApp', body: 'Chat tim kami, fast response.' },
	{ n: '2', title: 'Ceritakan kebutuhan Anda', body: 'Jelaskan situasi rumah atau kantor.' },
	{ n: '3', title: 'Terima estimasi', body: 'Estimasi harga transparan.' },
	{ n: '4', title: 'Tim datang', body: 'Tim profesional datang sesuai jadwal.' },
	{ n: '5', title: 'Rumah kembali bersih', body: 'Nikmati hasilnya, siap digunakan.' },
];

export const reviews: Review[] = [
	{ name: 'Dewi A.', area: 'BSD', text: 'Baru pindah dan rumah langsung bersih maksimal. Timnya teliti banget.' },
	{ name: 'Reza P.', area: 'Jakarta Selatan', text: 'Setelah renovasi parah debunya. Tentram beresin sampai bersih, siap ditempati.' },
	{ name: 'Sinta M.', area: 'Gading Serpong', text: 'Pakai layanan rutin. Selalu tepat waktu dan hasilnya konsisten.' },
];

export const areas: string[] = [
	'Jakarta', 'BSD', 'Alam Sutera', 'Gading Serpong', 'Bekasi', 'Depok', 'Tangerang', 'Cibubur', 'Bogor', 'dan area lainnya',
];

export const faqs: Faq[] = [
	{ q: 'Apakah tim membawa alat sendiri?', a: 'Ya. Tim Tentram datang dengan peralatan lengkap, Anda tidak perlu menyiapkan apa pun.' },
	{ q: 'Berapa lama proses cleaning?', a: 'Tergantung luas dan kondisi ruangan. Home cleaning biasanya 3–5 jam, deep cleaning bisa lebih lama. Estimasi pasti diberikan saat booking.' },
	{ q: 'Bagaimana menentukan harga?', a: 'Harga disesuaikan dengan luas area, jenis layanan, dan kondisi. Semua transparan, tanpa biaya tersembunyi.' },
	{ q: 'Apakah bisa datang di akhir pekan?', a: 'Bisa. Kami menyediakan jadwal fleksibel termasuk akhir pekan sesuai ketersediaan.' },
	{ q: 'Bagaimana jika saya tidak puas?', a: 'Setiap pekerjaan mengikuti quality checklist. Jika ada yang tidak sesuai, hubungi kami dan kami akan menindaklanjutinya.' },
];