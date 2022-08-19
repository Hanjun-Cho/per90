module.exports = {
  content: ["./src/templates/**/**.{html,js}"],
  theme: {
    extend: {},
    colors: {
      'white':'#FFFFFF',
      'blue':'#002E62',
      'blue2':'#5193BC',
      'dark_blue':'#00234A',
      'yellow':'#E9E9A8',
      'green':'#B9FBB9',
      'red':'#FFBFBF',
      'purple':'#E8BFFF',
      'pink':'#FFBFDB'
    },
    screens: {
      'large':{'min':'1450px'},
      'medium':{'max':'1449px'},
      'mini':{'max':'899px'}
    },
  },
  plugins: [],
}
